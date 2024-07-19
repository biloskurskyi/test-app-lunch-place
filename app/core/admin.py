"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user."""
    ordering = ['id']
    list_display = ['email', 'name', 'is_active', 'is_superuser']
    search_fields = ['email', 'name', 'is_active', 'is_superuser']
    readonly_fields = ['email', 'name', ]
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('email', 'name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(models.User, UserAdmin)


class LunchAdmin(admin.ModelAdmin):
    """Define the lunch info from restaurants"""

    ordering = ['id']
    all = ['menu', 'user', 'day']
    list_display = all
    search_fields = ['menu', 'day']
    readonly_fields = all
    list_per_page = 10


admin.site.register(models.Lunch, LunchAdmin)


class LunchVotingAdmin(admin.ModelAdmin):
    """Define the lunch orders for every day"""

    ordering = ['id']
    all = ['lunch', 'date', 'user']
    list_display = all
    search_fields = ['date']
    readonly_fields = all
    list_per_page = 10


admin.site.register(models.LunchVoting, LunchVotingAdmin)


class LunchReportAdmin(admin.ModelAdmin):
    """Define the report for every day"""

    ordering = ['id']
    all = ['lunch', 'date', 'count']
    list_display = all
    search_fields = ['date', 'count']
    readonly_fields = all
    list_per_page = 10


admin.site.register(models.LunchReport, LunchReportAdmin)
