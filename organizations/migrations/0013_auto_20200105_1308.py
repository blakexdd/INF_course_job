# Generated by Django 2.2.7 on 2020-01-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0012_auto_20191220_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='brief_description',
            field=models.CharField(default='Auto', max_length=500),
        ),
        migrations.AlterField(
            model_name='organization',
            name='location',
            field=models.CharField(default='Auto', max_length=70),
        ),
        migrations.AlterField(
            model_name='organization',
            name='year_of_est',
            field=models.CharField(default='Auto', max_length=10),
        ),
    ]
