from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter by employee if provided
        employee_id = self.request.query_params.get('employee_id')
        
        queryset = PerformanceReview.objects.all()
        
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        
        # Admins can see all reviews, managers their department's reviews, employees only their own reviews
        elif self.request.user.role == 'manager' and hasattr(self.request.user, 'employee_profile'):
            return queryset.filter(
                employee__department=self.request.user.employee_profile.department
            )
        elif hasattr(self.request.user, 'employee_profile'):
            return queryset.filter(employee__user=self.request.user)
        return PerformanceReview.objects.none()
    
    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        review = self.get_object()
        new_stage = request.data.get('stage')
        
        if not new_stage:
            return Response(
                {'error': 'Stage is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare kwargs for transition
        kwargs = {}
        if new_stage == 'review_scheduled':
            kwargs['scheduled_date'] = request.data.get('scheduled_date')
        elif new_stage == 'feedback_provided':
            kwargs['feedback'] = request.data.get('feedback')
            if hasattr(request.user, 'employee_profile'):
                kwargs['reviewed_by'] = request.user.employee_profile
        elif new_stage in ['review_approved', 'review_rejected']:
            if hasattr(request.user, 'employee_profile'):
                kwargs['approved_by'] = request.user.employee_profile
        
        if review.transition_to(new_stage, **kwargs):
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        else:
            return Response(
                {'error': f'Invalid transition from {review.stage} to {new_stage}'},
                status=status.HTTP_400_BAD_REQUEST
            )