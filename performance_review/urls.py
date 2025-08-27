from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PerformanceReviewViewSet

router = routers.DefaultRouter()
router.register('performance-reviews', PerformanceReviewViewSet)

urlpatterns = [
    path('performance-reviews/', include(router.urls)),
]