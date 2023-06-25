from django.db import models
from authentication.models import Seller

class Property(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    square_feet = models.PositiveIntegerField()
    overview = models.TextField()
    bhk = models.CharField(max_length=10)
    nearby_hospitals = models.CharField(max_length=100)
    nearby_schools = models.CharField(max_length=100)
    nearby_police_station = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    
    #image will be uploaded to MEDIA_ROOT / property pictures
    pictures = models.ImageField(upload_to='property_images/')

    class Meta:
        verbose_name_plural = "properties"


    def __str__(self):
        return self.address





# Create your models here.
