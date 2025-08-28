
from django.urls import path, include
from rest_framework import routers

from .views import CompanyViewSet, DepartmentViewSet, ProjectViewSet
from .views import CompanyAdminViewSet, DepartmentAdminViewSet, ProjectAdminViewSet



admin_router = routers.DefaultRouter()
admin_router.register('companies_panel', CompanyAdminViewSet, basename='admin-company')
admin_router.register('departments_panel', DepartmentAdminViewSet, basename='admin-department')
admin_router.register('projects_panel', ProjectAdminViewSet, basename='admin-project')

router = routers.DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('departments', DepartmentViewSet, basename='department')
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('admin-panel/', include(admin_router.urls)),
    path('', include(router.urls)),
]