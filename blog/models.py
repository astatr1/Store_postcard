from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique_for_date='time_published',
                            verbose_name='Slug')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField(verbose_name='Тело поста')
    time_published = models.DateTimeField(default=timezone.now,
                                          verbose_name='Время публикации')
    time_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True,
                                        verbose_name='Время обновления')
    is_published = models.BooleanField(choices=tuple(
        map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT, verbose_name='Статус')
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-time_published']
        indexes = [
            models.Index(fields=['-time_published']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.time_published.year,
                                                 self.time_published.month,
                                                 self.time_published.day,
                                                 self.slug])


class Comment(models.Model):
    class Status(models.IntegerChoices):
        BLOCKED = 0, 'Заблокировано'
        PUBLISHED = 1, 'Опубликовано'

    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пост')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    body = models.TextField(max_length=500, verbose_name='Комментарий')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_active = models.BooleanField(choices=tuple(
        map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.PUBLISHED, verbose_name='Статус')

    class Meta:
        ordering = ['time_created']
        indexes = [models.Index(fields=['time_created']),]

    def __str__(self):
        return f'Комментарий {self.name} к посту {self.post}'