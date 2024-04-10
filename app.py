#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from requests import get
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:steve@localhost/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('tenant'))  # Redirect to tenant page after login
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/tenant')
@login_required
def tenant():
    # Make API call to get tenant property data
    api_tenant = 'https://your_tenant_api_url'
    response_tenant = get(api_tenant)
    data_tenant = json.loads(response_tenant.text)
    return render_template('tenant.html', properties=data_tenant)

@app.route('/landlord')
@login_required
def landlord():
    # Make API call to get landlord property data
    api_landlord = 'https://your_landlord_api_url'
    response_landlord = get(api_landlord)
    data_landlord = json.loads(response_landlord.text)
    return render_template('landlord.html', properties=data_landlord)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        flash('New user has been created.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
