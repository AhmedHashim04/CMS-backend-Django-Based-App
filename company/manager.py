from user.models import Employee, User
from company.models import PerformanceReview

from .serializers import PerformanceReviewSerializer


from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.urls import path

# Example role-checking helpers
def is_manager(user):
    return hasattr(user, 'employee') and user.employee.role == 'manager'

def is_employee(user):
    return hasattr(user, 'employee') and user.employee.role == 'employee'

def can_view_review(user, review):
    # Managers can view all, employees only their own
    return is_manager(user) or (is_employee(user) and review.employee.user == user)

def can_edit_review(user, review):
    # Only managers can edit unless it's feedback stage, then employee can add feedback
    if is_manager(user):
        return True
    if is_employee(user) and review.status == review.ReviewStatus.FEEDBACK and review.employee.user == user:
        return True
    return False

def schedule_review(manager_user, employee, project, scheduled_date):
    if not is_manager(manager_user):
        raise PermissionDenied("Only managers can schedule reviews.")
    review = PerformanceReview.objects.create(
        employee=employee,
        project=project,
        scheduled_date=scheduled_date,
        status=PerformanceReview.ReviewStatus.SCHEDULED
    )
    return review

def provide_feedback(employee_user, review, feedback_text):
    if not (is_employee(employee_user) and review.employee.user == employee_user):
        raise PermissionDenied("Only the assigned employee can provide feedback.")
    if review.status != PerformanceReview.ReviewStatus.FEEDBACK:
        raise PermissionDenied("Feedback can only be provided at the feedback stage.")
    review.feedback = feedback_text
    review.transition_status(PerformanceReview.ReviewStatus.UNDER_APPROVAL)
    review.save()
    return review

def approve_review(manager_user, review):
    if not is_manager(manager_user):
        raise PermissionDenied("Only managers can approve reviews.")
    if review.status != PerformanceReview.ReviewStatus.UNDER_APPROVAL:
        raise PermissionDenied("Review must be under approval to approve.")
    review.transition_status(PerformanceReview.ReviewStatus.APPROVED)
    review.save()
    return review

def reject_review(manager_user, review):
    if not is_manager(manager_user):
        raise PermissionDenied("Only managers can reject reviews.")
    if review.status != PerformanceReview.ReviewStatus.UNDER_APPROVAL:
        raise PermissionDenied("Review must be under approval to reject.")
    review.transition_status(PerformanceReview.ReviewStatus.REJECTED)
    review.save()
    return review

def view_review(user, review_id):
    review = PerformanceReview.objects.get(id=review_id)
    if not can_view_review(user, review):
        raise PermissionDenied("You do not have access to this review.")
    return review

class PerformanceReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if is_manager(user):
            return PerformanceReview.objects.all()
        elif is_employee(user):
            return PerformanceReview.objects.filter(employee__user=user)
        return PerformanceReview.objects.none()
    def perform_create(self, serializer):
        user = self.request.user
        employee_slug = self.request.data.get('employee')
        project = self.request.data.get('project')
        scheduled_date = self.request.data.get('scheduled_date')
        try:
            employee = Employee.objects.get(slug=employee_slug)
            review = schedule_review(user, employee, project, scheduled_date)
            serializer.instance = review
        except Employee.DoesNotExist:
            raise PermissionDenied("Employee not found.")
        except PermissionDenied as e:
            raise PermissionDenied(str(e))

class PerformanceReviewDetailView(generics.RetrieveAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if is_manager(user):
            return PerformanceReview.objects.all()
        elif is_employee(user):
            return PerformanceReview.objects.filter(employee__user=user)
        return PerformanceReview.objects.none()
    def get_object(self):
        review = super().get_object()
        if not can_view_review(self.request.user, review):
            raise PermissionDenied("You do not have access to this review.")
        return review

class ProvideFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        review = get_object_or_404(PerformanceReview, pk=pk)
        feedback_text = request.data.get('feedback')
        try:
            provide_feedback(request.user, review, feedback_text)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        serializer = PerformanceReviewSerializer(review)
        return Response(serializer.data)

class ApproveReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        review = get_object_or_404(PerformanceReview, pk=pk)
        try:
            approve_review(request.user, review)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        serializer = PerformanceReviewSerializer(review)
        return Response(serializer.data)

class RejectReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        review = get_object_or_404(PerformanceReview, pk=pk)
        try:
            reject_review(request.user, review)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        serializer = PerformanceReviewSerializer(review)
        return Response(serializer.data)

urlpatterns = [
    path('performance-reviews/', PerformanceReviewListCreateView.as_view(), name='performance-review-list-create'),
    path('performance-reviews/<int:pk>/', PerformanceReviewDetailView.as_view(), name='performance-review-detail'),
    path('performance-reviews/<int:pk>/provide-feedback/', ProvideFeedbackView.as_view(), name='performance-review-provide-feedback'),
    path('performance-reviews/<int:pk>/approve/', ApproveReviewView.as_view(), name='performance-review-approve'),
    path('performance-reviews/<int:pk>/reject/', RejectReviewView.as_view(), name='performance-review-reject'),
]