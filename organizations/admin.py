from django.contrib import admin
from .models import Organization
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    models = Organization
    list_display = ('name', 'year_of_est')

admin.site.register(Organization, PostAdmin)