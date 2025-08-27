from django.db import models
from user.models import Employee

class PerformanceReview(models.Model):
    REVIEW_STAGES = (
        ('pending_review', 'Pending Review'),
        ('review_scheduled', 'Review Scheduled'),
        ('feedback_provided', 'Feedback Provided'),
        ('under_approval', 'Under Approval'),
        ('review_approved', 'Review Approved'),
        ('review_rejected', 'Review Rejected'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    stage = models.CharField(max_length=20, choices=REVIEW_STAGES, default='pending_review')
    scheduled_date = models.DateTimeField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_conducted')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Performance Review - {self.employee.user.get_full_name()} - {self.get_stage_display()}"
    
    def can_transition_to(self, new_stage):
        transitions = {
            'pending_review': ['review_scheduled'],
            'review_scheduled': ['feedback_provided'],
            'feedback_provided': ['under_approval'],
            'under_approval': ['review_approved', 'review_rejected'],
            'review_rejected': ['feedback_provided'],
            'review_approved': []  # No transitions after approval
        }
        return new_stage in transitions.get(self.stage, [])
    
    def transition_to(self, new_stage, **kwargs):
        if self.can_transition_to(new_stage):
            self.stage = new_stage
            
            if new_stage == 'review_scheduled' and 'scheduled_date' in kwargs:
                self.scheduled_date = kwargs['scheduled_date']
            
            if new_stage == 'feedback_provided' and 'feedback' in kwargs:
                self.feedback = kwargs['feedback']
                if 'reviewed_by' in kwargs:
                    self.reviewed_by = kwargs['reviewed_by']
            
            if new_stage in ['review_approved', 'review_rejected'] and 'approved_by' in kwargs:
                self.approved_by = kwargs['approved_by']
            
            self.save()
            return True
        return False