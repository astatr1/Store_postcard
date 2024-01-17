from django.db import models
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('store:store_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Postcard(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    category = models.ForeignKey(Category, related_name='postcard', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение')
    content = models.TextField(blank=True, verbose_name='Описание открытки')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Наличие товара')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    time_published = models.DateTimeField(default=timezone.now, verbose_name='Время публикации')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.DRAFT, verbose_name='Статус')

    class Meta:
        ordering = ['title']
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['title']),
                   models.Index(fields=['-time_created'])]
        verbose_name = 'Открытка'
        verbose_name_plural = 'Открытки'

    def get_absolute_url(self):
        return reverse('store:postcard_detail', args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)