
from django.urls import path
from .views import CompanyViewSet, DepartmentViewSet, ProjectViewSet


urlpatterns = [

    path('companies/', CompanyViewSet.as_view(), name='company-list'),
    path('companies/<slug:slug>/', CompanyViewSet.as_view(), name='company-detail'),

    path('departments/', DepartmentViewSet.as_view(), name='department-list'),
    path('departments/<slug:slug>/', DepartmentViewSet.as_view(), name='department-detail'),

    path('projects/', ProjectViewSet.as_view(), name='project-list'),
    path('projects/<slug:slug>/', ProjectViewSet.as_view(), name='project-detail'),

]
