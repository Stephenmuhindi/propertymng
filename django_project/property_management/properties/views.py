from django.shortcuts import render
from .models import Landlord, Tenant, Property

def landlord_dashboard(request, landlord_id):
    landlord = Landlord.objects.get(id=landlord_id)
    properties = Property.objects.filter(landlord=landlord)
    occupied_properties = properties.filter(is_occupied=True).count()
    vacant_properties = properties.filter(is_occupied=False).count()
    context = {
        'landlord': landlord,
        'properties': properties,
        'occupied_properties': occupied_properties,
        'vacant_properties': vacant_properties,
    }
    return render(request, 'properties/landlord_dashboard.html', context)

def tenant_dashboard(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    context = {
        'tenant': tenant,
    }
    return render(request, 'properties/tenant_dashboard.html', context)
