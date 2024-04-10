from django.db import models

class Landlord(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

class Tenant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    rent_due_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.name
