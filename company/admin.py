from django.contrib import admin
from .models import Company, Department, Project

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'department_count', 'employee_count', 'project_count']
    readonly_fields = ['department_count', 'employee_count', 'project_count']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'employee_count', 'project_count']
    list_filter = ['company']
    readonly_fields = ['employee_count', 'project_count']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'department', 'start_date', 'end_date']
    list_filter = ['company', 'department']
    filter_horizontal = ['assigned_employees']