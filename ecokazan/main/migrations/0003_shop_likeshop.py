# Generated by Django 4.2.6 on 2023-11-23 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_recyclingcenter_district_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название магазина')),
                ('description', models.TextField(max_length=3000, verbose_name='Описание')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('working_hours', models.CharField(max_length=100, verbose_name='График работы')),
                ('vk_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на вк')),
                ('tg_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на тг')),
                ('website_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='LikeShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='main.shop', verbose_name='Магазин')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'db_table': 'like_shop',
            },
        ),
    ]
