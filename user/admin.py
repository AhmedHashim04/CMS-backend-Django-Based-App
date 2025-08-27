from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Employee

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'department', 'position', 'get_days_employed']
    list_filter = ['company', 'department', 'position']
    readonly_fields = ['get_days_employed']
admin.site.register(User, CustomUserAdmin)