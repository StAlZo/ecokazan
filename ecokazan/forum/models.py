from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Articles(models.Model):

    class ArticlesManager(models.Manager):
        def detail(self):
            return self.get_queryset() \
                .prefetch_related('save_event',)

    picture = models.ImageField(upload_to='images/articles_pictures', blank=True, null=True, verbose_name='Фото')
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    full_text = models.TextField(verbose_name="Описание", max_length=3000)
    mesto = models.TextField(verbose_name="Место проведения")
    data = models.DateTimeField(verbose_name="Дата")

    def get_sum_saves(self):
        return self.save_event.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_absolute_url(self):
        return reverse('forum-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="comments", verbose_name="Новость")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор")
    content = models.TextField(max_length=3000, verbose_name="Текст комментария")
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)

    class Meta:
        db_table = 'comments'
        indexes = [models.Index(fields=['-time_create', 'time_update'])]
        ordering = ['time_create']
        verbose_name = 'Комментарий новости'
        verbose_name_plural = 'Комментарии новости'

    def __str__(self):
        return f'{self.author}:{self.content}'


class SaveEvent(models.Model):
    event = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="save_event", verbose_name="Статья")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="save_event", verbose_name="Пользователь")
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    class Meta:
        db_table = "save_event"
        unique_together = ('event', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create'])]
        verbose_name = 'Сохранение события'
        verbose_name_plural = 'Сохраненные события'
