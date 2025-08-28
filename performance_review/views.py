from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer

from rest_framework import viewsets, permissions, status

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_slug = self.request.query_params.get('employee_slug')
        queryset = PerformanceReview.objects.all()
        if employee_slug:
            queryset = queryset.filter(employee__slug=employee_slug)
        return queryset

    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        review = self.get_object()
        new_stage = request.data.get('stage')

        try:
            review.transition_to(new_stage, **request.data)
            return Response(
                {"detail": f"Transitioned to {new_stage} successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
