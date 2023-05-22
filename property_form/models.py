from django.db import models
from authentication.models import Seller

class Property(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    square_feet = models.PositiveIntegerField()
    overview = models.TextField()
    nearby_schools = models.ManyToManyField('School', related_name='properties')
    nearby_police_stations = models.ManyToManyField('PoliceStation', related_name='properties')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ImageField(upload_to='property_pictures/')

    class Meta:
        verbose_name_plural = "properties"


    def __str__(self):
        return self.address

class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    distance = models.FloatField()

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name




# Create your models here.
