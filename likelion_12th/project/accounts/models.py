from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    GENDER_M = "male"
    GENDER_F = "female"
    
    GENDER_CHOICES = (
    	(GENDER_M, "Male"),
        (GENDER_F, "Female"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255)
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()