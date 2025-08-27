
from django.urls import path
from .views import EmployeeViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # login → access + refresh
    TokenRefreshView,     # refresh access
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh
    path('employees/', EmployeeViewSet.as_view(), name='employee-list'),
    path('employees/<slug:slug>/', EmployeeViewSet.as_view(), name='employee-detail'),
]
