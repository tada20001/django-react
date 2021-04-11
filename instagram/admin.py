from django.contrib import admin
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'caption', 'photo', 'location']




@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']