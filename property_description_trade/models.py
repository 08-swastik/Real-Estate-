from django.db import models


from property_form.models import Property


class ConfirmationData(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields as needed

    def __str__(self):

        return f"Confirmation for {self.property}"

# Create your models here.
