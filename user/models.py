from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role="employee", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password, role="manager", **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class ROLES(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        EMPLOYEE = 'employee', 'Employee'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES.choices)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email

class Employee(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
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

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLES.EMPLOYEE:
        Employee.objects.create(user=instance)

