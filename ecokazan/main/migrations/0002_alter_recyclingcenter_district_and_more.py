# Generated by Django 4.2.6 on 2023-11-22 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclingcenter',
            name='district',
            field=models.CharField(choices=[('Советский', 'Советский'), ('Приволжский', 'Приволжский'), ('Вахитовский', 'Вахитовский'), ('Московский', 'Московский'), ('Авиастроительный', 'Авиастроительный'), ('Ново-Савиновский', 'Ново Савиновский'), ('Кировский', 'Кировский')], max_length=70, verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='recyclingcenter',
            name='recycling_type',
            field=models.CharField(choices=[('Макулатура', 'Макулатура'), ('Металлолом', 'Металлолом'), ('Аккумуляторы', 'Аккумуляторы'), ('Одежда', 'Одежда'), ('Батарейки', 'Батарейки'), ('Пластик', 'Пластик'), ('Стеклотара', 'Стеклотара'), ('Техника', 'Техника')], max_length=100, verbose_name='Тип переработки'),
        ),
    ]
