#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from requests import get
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, EqualTo, Length
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import login_user, logout_user, login_required

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/flask_app_db'
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

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not login_user():
            return redirect(url_for('login'))
        return f(*args, **kwargs)

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
            return redirect(url_for('properties'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/tenant', methods=['GET'])
@login_required
def tenant():
    # Make API call to get property data
    api = 'https://your_tenant_api_url'
    response = get(api)
    properties = json.loads(response.text)
    return render_template('tenant.html', properties=properties)

@app.route('/landlord', methods=['GET'])
@login_required
def landlord():
    # Make API call to get property data
    api = 'https://your_landlord_api_url'
    response = get(api)
    properties = json.loads(response.text)
    return render_template('landlord.html', properties=properties)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully.')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            flash('Error while registering user: {}'.format(str(e)))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host="0.0.0.0")
