from django.db import models


# Create your models here.
class Post(models.Model):
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.link
