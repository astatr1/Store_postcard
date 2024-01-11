from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, verbose_name='Slug')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField(verbose_name='Тело поста')
    time_published = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(choices=tuple(
        map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT, verbose_name='Статус')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-time_published']
        indexes = [
            models.Index(fields=['-time_published']),
        ]

    def __str__(self):
        return self.title
