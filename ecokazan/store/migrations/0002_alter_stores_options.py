# Generated by Django 4.2.6 on 2023-11-08 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stores',
            options={'verbose_name': 'Магазин', 'verbose_name_plural': 'Магазины'},
        ),
    ]