# Generated by Django 2.2.7 on 2019-12-03 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20191201_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='days',
        ),
        migrations.AddField(
            model_name='person',
            name='days',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organizations.Dates'),
        ),
    ]