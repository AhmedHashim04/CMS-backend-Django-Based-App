from django.shortcuts import render
from .models import Employee

from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from .serializers import EmployeeSerializer
"""
iii. Employee
• POST: Create a new employee
• GET: Retrieve a single employee or list all employees
• PATCH: Update an existing employee
• DELETE: Delete an employee
"""

class EmployeeViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """
    API view set for managing Employee instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all employees.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single employee by ID.
        - CreateAPIView: Provides a create endpoint to add a new employee.
        - RetrieveUpdateDestroyAPIView: Provides endpoints to retrieve, update, or delete an employee.

    Attributes:
        queryset (QuerySet): All Employee objects from the database.
        serializer_class (Serializer): Serializer class used for Employee objects.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'