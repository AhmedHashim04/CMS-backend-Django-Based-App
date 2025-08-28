
from django.urls import path, include
from .views import  RegisterView, EmployeeViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # login → access + refresh
    TokenRefreshView,     # refresh access
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh

]
from rest_framework import routers

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
urlpatterns += [
    path('', include(router.urls)),
]
