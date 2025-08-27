from django.contrib import admin
from .models import PerformanceReview

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'stage', 'scheduled_date', 'reviewed_by', 'approved_by']
    list_filter = ['stage', 'scheduled_date']
    readonly_fields = ['created_at', 'updated_at']