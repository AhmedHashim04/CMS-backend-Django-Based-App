
from django.urls import path
from .views import EmployeeViewSet


urlpatterns = [

    path('employees/', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'}), name='employee-list'),
    path('employees/<slug:slug>/', EmployeeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}), name='employee-detail'),

]
