# Generated by Django 2.2.7 on 2019-12-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0010_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=150)),
            ],
        ),
    ]
