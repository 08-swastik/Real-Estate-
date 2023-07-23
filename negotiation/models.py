from django.db import models
from authentication.models import User

class Negotiation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    requested_price = models.CharField(max_length=20)


def __str__(self):
        return f"{self.first_name} {self.last_name}"