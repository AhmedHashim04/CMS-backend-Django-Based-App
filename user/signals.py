
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Employee

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLES.EMPLOYEE:
        Employee.objects.create(user=instance)

