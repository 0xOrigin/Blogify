from django.contrib import admin
from django.conf import settings
from django.utils import timezone


class BaseAdmin(admin.ModelAdmin):
    list_display = ['id',]
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by',]
    list_per_page = settings.PAGINATION_ADMIN_PAGE_SIZE

    def save_model(self, request, obj, form, change):
        if not obj.created_at:
            obj.created_at = timezone.now()
            obj.created_by = request.user
        else:
            obj.updated_at = timezone.now()
            obj.updated_by = request.user
        obj.save()
