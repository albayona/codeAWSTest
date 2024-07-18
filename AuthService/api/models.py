import uuid

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    iss = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255)

