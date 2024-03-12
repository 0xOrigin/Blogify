from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.conf import settings
from core.admin import BaseAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseAdmin):
    list_display = ('username', 'email', 'last_login', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'created_at', 'updated_at', 'created_by', 'updated_by',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates & logs', {
                'fields': ('last_login', 'created_at', 'updated_at', 'created_by', 'updated_by',),
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
    ) 
    exclude = ()

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    list_per_page = settings.PAGINATION_ADMIN_PAGE_SIZE
