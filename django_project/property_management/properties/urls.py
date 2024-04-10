from django.urls import path
from . import views


urlpatterns = [
    path('landlord/<int:landlord_id>/dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('tenant/<int:tenant_id>/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('', views.landing_page, name='landing_page')
]
