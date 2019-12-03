from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

# creating dates model
class Dates(models.Model):
    # creating day of the week
    day = models.CharField(max_length=20)

    # creating start time of the day
    start = models.CharField(max_length=5)

    # creating end time of the day
    end = models.CharField(max_length=5)

# creating persens model
class Person(models.Model):
    # creating name of the person
    name = models.CharField(max_length=20)

    # creating surname of the person
    surname = models.CharField(max_length=20)

    # creating middlename of the person
    middlename = models.CharField(max_length=20)

    # creating date of birth of the person
    date_of_birth = models.CharField(max_length=10)

    # creating post of the person
    post = models.CharField(max_length=20)

    # creating amount of hours per week
    hours_per_week = models.IntegerField()

    # creating days of work
    #days = models.ForeignKey('Dates', on_delete=models.SET_NULL, null=True)
    days = models.ManyToManyField(Dates)


# creating organization model
class Organization(models.Model):
    # creating name of organization
    name = models.CharField(max_length=20)

    # creating year of establishing organiazation
    year_of_est = models.CharField(max_length=10)

    # creating location of organization
    location = models.CharField(max_length=40, default='St. Petersburg')

    # creating brief description of organization
    brief_description = models.CharField(max_length=150, default='Some organization')

    # creating persons working in the company
    person = models.ManyToManyField(Person)



