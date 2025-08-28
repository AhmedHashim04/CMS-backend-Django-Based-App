from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer,PerformanceReviewCreateSerializer
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

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

class PerformanceReviewTransitionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            review = PerformanceReview.objects.get(id=pk)
            new_stage = request.data.get('stage')
            review.transition_to(new_stage, **request.data)
            return Response(
                {"detail": f"Transitioned to {new_stage} successfully."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

