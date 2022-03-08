from unicodedata import name
from django.db import models

# Create your models here.
# Guest -- hall ---reservation

class Movie(models.Model):
      hall=models.CharField(max_length=10)
      movie=models.CharField(max_length=10)
      date= models.DateField()

class Guest(models.Model):
      name = models.CharField(max_length=10)
      mobile = models.CharField(max_length=10)
class Reservation(models.Model):
      guest = models.ForeignKey(Guest,related_name="reservation",on_delete=models.CASCADE) 
      movie = models.ForeignKey(Movie,related_name="reservation",on_delete=models.CASCADE)     