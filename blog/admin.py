from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'time_published', 'is_published']
    list_filter = ['is_published', 'time_created', 'time_published', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'time_published'
    ordering = ['is_published', 'time_published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'time_created', 'time_updated']
    list_filter = ['is_active', 'time_created', 'time_updated']
    search_fields = ['name', 'email', 'body']
