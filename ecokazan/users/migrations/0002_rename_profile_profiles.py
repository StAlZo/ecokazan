# Generated by Django 4.2.6 on 2023-11-23 14:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Profiles',
        ),
    ]
