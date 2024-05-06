from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_M = "male"
    GENDER_F = "female"
    
    GENDER_CHOICES = (
    	(GENDER_M, "Male"),
        (GENDER_F, "Female"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255)