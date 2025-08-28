from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer, PerformanceReviewCreateSerializer, PerformanceReviewTransitionSerializer
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView

class PerformanceReviewListCreateView(generics.ListCreateAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_slug = self.request.query_params.get('employee_slug')
        queryset = PerformanceReview.objects.all()
        if employee_slug:
            queryset = queryset.filter(employee__slug=employee_slug)
        return queryset

class PerformanceReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class PerformanceReviewTransitionView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewTransitionSerializer

    def post(self, request, pk):
        review = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.transition_to(serializer.validated_data.pop('stage'), **serializer.validated_data)
        return Response(
            {"detail": f"Transitioned to {serializer.validated_data.get('stage')} successfully."},
            status=status.HTTP_200_OK
        )