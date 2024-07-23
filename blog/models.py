from django.db import models

from main.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/images', verbose_name='Изображение (превью)', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
