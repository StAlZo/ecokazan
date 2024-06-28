from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Stores(models.Model):
    class StoresManager(models.Manager):
        def detail(self):
            return self.get_queryset() \
                .prefetch_related('likes', 'ratings')

    picture = models.ImageField(upload_to='images/stores_pictures', blank=True, null=True, verbose_name='Фото')
    name = models.CharField(verbose_name="Название магазина", max_length=100)
    full_text = models.TextField(max_length=3000, verbose_name="Описание")
    adres = models.TextField(verbose_name="Адрес")
    timejob = models.TextField(verbose_name="График работы")
    vk_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на вк')
    tg_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на тг')
    website_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт')

    def get_sum_likes(self):
        return self.likes.count()

    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()]) #/ self.ratings.count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def get_absolute_url(self):
        return reverse('store-detail', kwargs={'pk': self.pk})


class LikeStore(models.Model):
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name="likes", verbose_name="Магазин")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="Пользователь")
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.store.name} - {self.user.username}"

    class Meta:
        db_table = "like_store"
        unique_together = ('store', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class RatingStore(models.Model):
    store = models.ForeignKey(Stores, on_delete=models.CASCADE, related_name="ratings", verbose_name="Магазин")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings", verbose_name="Пользователь")
    value = models.IntegerField(verbose_name='Значение', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.store.name} - {self.user.username}: {self.value}"

    class Meta:
        db_table = "rating_store"
        unique_together = ('store', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'