from django.db import models
from authentication.models import User
from property_form.models import Property

class Negotiation(models.Model):

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    requested_price = models.CharField(max_length=20)
    status = models.CharField(max_length=10, blank=True, null=True)
    accepted_time = models.DateTimeField(null=True, blank=True)


def __str__(self):
        return f"{self.first_name} {self.last_name}"