from django.db import models
from authentication.models import Seller

class Property(models.Model):

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        
    )
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    square_feet = models.PositiveIntegerField()
    overview = models.TextField()
    bhk = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ImageField(upload_to='property_images/')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    

    class Meta:
        verbose_name_plural = "properties"


    def __str__(self):
        return self.address





# Create your models here.
