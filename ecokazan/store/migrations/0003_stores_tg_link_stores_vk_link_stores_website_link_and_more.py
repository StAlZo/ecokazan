# Generated by Django 4.2.6 on 2023-11-23 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_alter_stores_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='stores',
            name='tg_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на тг'),
        ),
        migrations.AddField(
            model_name='stores',
            name='vk_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на вк'),
        ),
        migrations.AddField(
            model_name='stores',
            name='website_link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт'),
        ),
        migrations.AlterField(
            model_name='stores',
            name='full_text',
            field=models.TextField(max_length=3000, verbose_name='Описание'),
        ),
        migrations.CreateModel(
            name='LikeStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='store.stores', verbose_name='Магазин')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
                'db_table': 'like_store',
            },
        ),
    ]
