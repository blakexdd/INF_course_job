# Generated by Django 2.2.7 on 2019-12-20 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0011_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='brief_description',
            field=models.CharField(default='Some organization', max_length=500),
        ),
        migrations.AlterField(
            model_name='organization',
            name='location',
            field=models.CharField(default='St. Petersburg', max_length=70),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
