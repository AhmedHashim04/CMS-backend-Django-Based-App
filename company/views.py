from .models import Company, Department, Project

from .serializers import CompanySerializer, DepartmentSerializer, ProjectSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


class CompanyViewSet(ListAPIView, RetrieveAPIView):
    """
    API view set for listing and retrieving Company instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all companies.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single company by slug.

    Attributes:
        queryset (QuerySet): All Company objects from the database.
        serializer_class (Serializer): Serializer class used for Company objects.
        permission_classes (list): List of permission classes to apply to the view.
        lookup_field (str): Field used to lookup Company instances.
    """

    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'


class DepartmentViewSet(ListAPIView, RetrieveAPIView):
    """
    API view set for listing and retrieving Department instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all departments.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single department by slug.

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'slug'


    Attributes:
        queryset (QuerySet): All Department objects from the database.
        serializer_class (Serializer): Serializer class used for Department objects.
        permission_classes (list): List of permission classes to apply to the view.
        lookup_field (str): Field used to lookup Department instances.
    """
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'slug'


class ProjectViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """
    API view set for managing Project instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all Projects.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single Project by slug.
        - CreateAPIView: Provides a create endpoint to add a new Project.
        - RetrieveUpdateDestroyAPIView: Provides endpoints to retrieve, update, or delete an Project.

    Attributes:
        queryset (QuerySet): All Project objects from the database.
        serializer_class (Serializer): Serializer class used for Project objects.
        permission_classes (list): List of permission classes to apply to the view.
        lookup_field (str): Field used to lookup Project instances.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

