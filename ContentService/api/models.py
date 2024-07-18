from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(('email address'), unique=True)
    name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    scraped_text = models.CharField(max_length=3000)
    liked = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    description = models.CharField(max_length=3000)
    date = models.DateField()
    price = models.FloatField()
    model = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    miles = models.IntegerField()
    link = models.CharField(unique=True, max_length=500)
    year = models.IntegerField()
    score = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.model


class AboutAttribute(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1500)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='about')

    def __str__(self):
        return self.text


class SellerAttribute(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1500)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='seller')

    def __str__(self):
        return self.text


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=1500)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.link
