from django.contrib import admin
from django.conf import settings
from core.admin import BaseAdmin
from blog.models import Post


@admin.register(Post)
class PostAdmin(BaseAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at',)
    search_fields = ('title', 'author__username',)
    list_filter = ('author',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by',)
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
