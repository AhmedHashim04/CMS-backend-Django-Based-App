from django.db import models
from user.models import Employee

class Company(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower()
        super().save(*args, **kwargs)

    @property
    def department_count(self):
        return self.departments.count()
    
    @property   
    def employee_count(self):
        return self.employees.count()
    
    @property   
    def project_count(self):
        return self.projects.count()


class Department(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower() + '-' + self.company.slug
        super().save(*args, **kwargs)

    @property
    def employee_count(self):
        return self.employees.count()

    @property
    def project_count(self):
        return self.projects.count()


class Project(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_employees = models.ManyToManyField(Employee, related_name='projects')

    def save(self, *args, **kwargs):
        self.slug = self.name.lower() + '-' + self.department.slug + '-' + self.company.slug
        super().save(*args, **kwargs)

