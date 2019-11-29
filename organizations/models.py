from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=20)
    year_of_est = models.CharField(max_length=10)


