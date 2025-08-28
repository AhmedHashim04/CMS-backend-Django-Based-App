from django.urls import path, include
from rest_framework import routers
from .views import PerformanceReviewViewSet

router = routers.DefaultRouter()
router.register('performance-reviews', PerformanceReviewViewSet, basename='performance-review')

urlpatterns = [
    path('performance-reviews/', include(router.urls)),
]