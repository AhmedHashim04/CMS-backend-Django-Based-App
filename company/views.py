from .models import Company, Department, Project, PerformanceReview
from user.models import Employee

from .serializers import CompanySerializer, DepartmentSerializer, ProjectSerializer, PerformanceReviewSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView



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


