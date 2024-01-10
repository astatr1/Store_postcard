# Generated by Django 4.2.8 on 2024-01-10 19:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('postcard', '0002_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcard',
            name='time_published',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время публикации'),
        ),
    ]
