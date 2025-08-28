from .models import Employee, User
from .serializers import UserRegisterSerializer
from rest_framework.generics import CreateAPIView
from .serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API view set for managing Employee instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all employees.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single employee by slug.
        - CreateAPIView: Provides a create endpoint to add a new employee.
        - RetrieveUpdateDestroyAPIView: Provides endpoints to retrieve, update, or delete an employee.

    Attributes:
        queryset (QuerySet): All Employee objects from the database.
        serializer_class (Serializer): Serializer class used for Employee objects.
        permission_classes (list): List of permission classes to apply to the view.
        lookup_field (str): Field used to lookup Department instances.
    """
    permission_classes = [IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'slug'


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
