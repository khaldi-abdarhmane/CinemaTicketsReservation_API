from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from tickets.models import Guest,Movie,Reservation

class MovieSerializer(serializers.ModelSerializer):
      class Meta:
            model= Movie
            fields='__all__'
class ReservationSerializer(serializers.ModelSerializer):
      class Meta:
            model= Reservation      
            fields='__all__'            
class GuestSerializer(serializers.ModelSerializer):
      class Meta:
            model= Guest      
            fields=['name','mobile','id'] 




