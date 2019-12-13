from django.forms import ModelForm
from .models import Organization, Person, Dates

class Editing_Organization(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'year_of_est', 'location',
                  'brief_description']

class Editing_Person(ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'surname', 'middlename',
                  'date_of_birth', 'post', 'hours_per_week']

class Editing_Days(ModelForm):
    class Meta:
        model = Dates
        fields = ['day', 'start', 'end']
