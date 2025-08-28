from django.urls import path, include
from .views import *


urlpatterns = [
    path('performance-reviews/', PerformanceReviewListCreateView.as_view(), name='performance-review-list-create'),
    path('performance-reviews/<uuid:pk>/', PerformanceReviewRetrieveUpdateDestroyView.as_view(), name='performance-review-detail'),
    path('performance-reviews/<uuid:pk>/transition/', PerformanceReviewTransitionView.as_view(), name='performance-review-transition'),
]