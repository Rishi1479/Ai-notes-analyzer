from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Section, Note


class UserAdmin(BaseUserAdmin):
    """Admin view for the custom User model with role field."""
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Section)
admin.site.register(Note)