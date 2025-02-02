# Generated by Django 4.2.6 on 2023-11-23 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_stores_tg_link_stores_vk_link_stores_website_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Значение')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
                'db_table': 'rating_store',
                'ordering': ('-time_create',),
            },
        ),
        migrations.AlterModelOptions(
            name='likestore',
            options={'ordering': ('-time_create',), 'verbose_name': 'Лайк', 'verbose_name_plural': 'Лайки'},
        ),
        migrations.AddField(
            model_name='likestore',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время добавления'),
        ),
        migrations.AlterUniqueTogether(
            name='likestore',
            unique_together={('store', 'user')},
        ),
        migrations.AddIndex(
            model_name='likestore',
            index=models.Index(fields=['-time_create'], name='like_store_time_cr_23edb4_idx'),
        ),
        migrations.AddField(
            model_name='ratingstore',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='store.stores', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='ratingstore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddIndex(
            model_name='ratingstore',
            index=models.Index(fields=['-time_create'], name='rating_stor_time_cr_6f9fc3_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='ratingstore',
            unique_together={('store', 'user')},
        ),
    ]
