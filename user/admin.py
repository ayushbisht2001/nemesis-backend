from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin 
from django.utils.translation import gettext, gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser 
    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address')}),
    (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
    }),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)