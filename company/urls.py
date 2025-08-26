
from django.urls import path
from .views import CompanyViewSet, DepartmentViewSet, ProjectViewSet


urlpatterns = [

    path('companies/', CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='company-list'),
    path('companies/<slug:slug>/', CompanyViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='company-detail'),

    path('departments/', DepartmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='department-list'),
    path('departments/<slug:slug>/', DepartmentViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='department-detail'),

    path('projects/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list'),
    path('projects/<slug:slug>/', ProjectViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-detail'),

]
