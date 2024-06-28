from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create your models here.

class RecyclingCenter(models.Model):

    class District(models.TextChoices):
        Советский = "Советский",
        Приволжский = "Приволжский",
        Вахитовский = "Вахитовский",
        Московский = "Московский",
        Авиастроительный = "Авиастроительный",
        Ново_Савиновский = "Ново-Савиновский"
        Кировский = "Кировский"

    class RecyclingType(models.TextChoices):
        Макулатура = "Макулатура",
        Металлолом = "Металлолом",
        Аккумуляторы = "Аккумуляторы",
        Одежда = "Одежда",
        Батарейки = "Батарейки",
        Пластик = "Пластик",
        Стеклотара = "Стеклотара",
        Техника = "Техника"

    title = models.CharField(max_length=255, verbose_name='Название')
    recycling_type = models.CharField(max_length=100, choices=RecyclingType.choices, verbose_name="Тип переработки")
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", unique=True)
    address = models.CharField(max_length=255, verbose_name='Адрес')
    district = models.CharField(max_length=70, choices=District.choices, verbose_name='Район')
    latitude = models.FloatField(verbose_name='Ширина')
    longitude = models.FloatField(verbose_name='Долгота')

    def __str__(self):
        return self.title

    def get_sum_favorites(self):
        return self.favorites_center.count()

    class Meta:
        verbose_name = 'Центр переработки'
        verbose_name_plural = 'Центры переработки'


class FavoritesRecyclingCenter(models.Model):
    recycling_center = models.ForeignKey(RecyclingCenter, on_delete=models.CASCADE, related_name="favorites_center", verbose_name="Центр переработки")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites_center", verbose_name="Пользователь")
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.recycling_center.title} - {self.user.username}"

    class Meta:
        db_table = "favorites_center"
        unique_together = ('recycling_center', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
