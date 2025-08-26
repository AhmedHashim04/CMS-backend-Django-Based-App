from .models import Company, Department, Project

from .serializers import CompanySerializer, DepartmentSerializer, ProjectSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView



class CompanyViewSet(ListAPIView, RetrieveAPIView):
    """
    API view set for listing and retrieving Company instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all companies.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single company by ID.

    Attributes:
        queryset (QuerySet): All Company objects from the database.
        serializer_class (Serializer): Serializer class used for Company objects.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'slug'


class DepartmentViewSet(ListAPIView, RetrieveAPIView):
    """
    API view set for listing and retrieving Department instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all departments.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single department by ID.

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'slug'


    Attributes:
        queryset (QuerySet): All Department objects from the database.
        serializer_class (Serializer): Serializer class used for Department objects.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'slug'


class ProjectViewSet(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    """
    API view set for managing Project instances.

    Inherits from:
        - ListAPIView: Provides a read-only endpoint to list all Projects.
        - RetrieveAPIView: Provides a read-only endpoint to retrieve a single Project by ID.
        - CreateAPIView: Provides a create endpoint to add a new Project.
        - RetrieveUpdateDestroyAPIView: Provides endpoints to retrieve, update, or delete an Project.

    Attributes:
        queryset (QuerySet): All Project objects from the database.
        serializer_class (Serializer): Serializer class used for Project objects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'