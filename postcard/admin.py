from django.contrib import admin
from .models import Category, Postcard


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Postcard)
class PostcardAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'available', 'time_created', 'time_updated']
    list_filter = ['available', 'time_created', 'time_updated']
    list_editable = ['available', 'price']
    prepopulated_fields = {'slug': ('title',)}