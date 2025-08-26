from datetime import date
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    slug = models.SlugField(unique=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey('company.Department', on_delete=models.CASCADE, related_name='employees')

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    position = models.CharField(max_length=100)
    hired_on = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        base = self.email.split('@')[0].lower()
        if Employee.objects.filter(slug=base).exists():
            base = f"{base}-{Employee.objects.filter(email=self.email).count()}"
        self.slug = base
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def get_days_employed(self):
        if self.hired_on:
            return (date.today() - self.hired_on).days
        return 0
