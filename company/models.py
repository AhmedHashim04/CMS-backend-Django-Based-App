from django.db import models
from user.models import Employee

class Company(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower()
        super().save(*args, **kwargs)

    @property
    def department_count(self):
        return self.departments.count()
    
    @property   
    def employee_count(self):
        return self.employees.count()
    
    @property   
    def project_count(self):
        return self.projects.count()


class Department(models.Model):
    slug = models.SlugField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower() + '-' + self.company.slug
        super().save(*args, **kwargs)

    @property
    def employee_count(self):
        return self.employees.count()

    @property
    def project_count(self):
        return self.projects.count()


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_employees = models.ManyToManyField(Employee, related_name='projects')

class PerformanceReview(models.Model):
    class ReviewStatus(models.TextChoices):
        PENDING = 'pending_review', 'Pending Review'
        SCHEDULED = 'review_scheduled', 'Review Scheduled'
        FEEDBACK = 'feedback_provided', 'Feedback Provided'
        UNDER_APPROVAL = 'under_approval', 'Under Approval'
        APPROVED = 'review_approved', 'Review Approved'
        REJECTED = 'review_rejected', 'Review Rejected'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='performance_reviews')

    scheduled_date = models.DateField(null=True, blank=True)
    
    feedback = models.TextField(blank=True)

    status = models.CharField(max_length=20,choices=ReviewStatus.choices,default=ReviewStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _TRANSITIONS = {
        ReviewStatus.PENDING: [ReviewStatus.SCHEDULED],
        ReviewStatus.SCHEDULED: [ReviewStatus.FEEDBACK],
        ReviewStatus.FEEDBACK: [ReviewStatus.UNDER_APPROVAL],
        ReviewStatus.UNDER_APPROVAL: [ReviewStatus.APPROVED, ReviewStatus.REJECTED],
        ReviewStatus.APPROVED: [],
        ReviewStatus.REJECTED: [],
    }

    def can_transition_to(self, new_status):
        return new_status in self._TRANSITIONS.get(self.status, [])
    
    def transition_status(self, new_status):
        if self.can_transition_to(new_status):
            self.status = new_status
            self.save(update_fields=['status', 'updated_at'])
            return True
        return False

    def __str__(self):
        return f"{self.employee} - {self.get_status_display()}"
    

# - Pending Review: Employee is flagged for performance review.
# - Review Scheduled: A review meeting has been scheduled.
# - Feedback Provided: Feedback from the review meeting has been documented.
# - Under Approval: Feedback is under managerial review.
# - Review Approved: Performance review is finalized and approved.
# - Review Rejected: Feedback is rejected and requires rework.

# Pending Review -> Review Scheduled -> Feedback Provided -> Under Approval -> Review Approved/Review Rejected

# - قيد المراجعة: تم تمييز الموظف لمراجعة الأداء.
# - تم جدولة المراجعة: تم تحديد موعد اجتماع المراجعة.
# - تم تقديم الملاحظات: تم توثيق الملاحظات من اجتماع المراجعة.
# - قيد الموافقة: الملاحظات قيد مراجعة الإدارة.
# - تمت الموافقة على المراجعة: تم الانتهاء من مراجعة الأداء والموافقة عليها.
# - تم رفض المراجعة: تم رفض الملاحظات وتتطلب إعادة العمل.

# قيد المراجعة -> تم جدولة المراجعة -> تم تقديم الملاحظات -> قيد الموافقة -> تمت الموافقة على المراجعة/تم رفض المراجعة
