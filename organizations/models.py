from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Organization(models.Model):
    # creating name of organization
    name = models.CharField(max_length=20)

    # creating year of establishing organiazation
    year_of_est = models.CharField(max_length=10)

    # creating location of organization
    location = models.CharField(max_length=40, default='St. Petersburg')

    # creating brief description of organization
    brief_description = models.CharField(max_length=150, default='Some organization')



