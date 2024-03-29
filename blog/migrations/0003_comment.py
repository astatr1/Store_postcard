# Generated by Django 4.2.8 on 2024-01-14 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('body', models.TextField(max_length=500, verbose_name='Комментарий')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('is_active', models.BooleanField(choices=[(False, 'Заблокировано'), (True, 'Опубликовано')], default=1, verbose_name='Статус')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Пост')),
            ],
            options={
                'ordering': ['time_created'],
                'indexes': [models.Index(fields=['time_created'], name='blog_commen_time_cr_838dd1_idx')],
            },
        ),
    ]
