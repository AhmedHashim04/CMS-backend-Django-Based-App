from rest_framework import serializers
from .models import PerformanceReview
from .serializers import EmployeeSerializer

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    reviewed_by_details = EmployeeSerializer(source='reviewed_by', read_only=True)
    approved_by_details = EmployeeSerializer(source='approved_by', read_only=True)
    
    class Meta:
        model = PerformanceReview
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        # Add validation for stage transitions
        instance = self.instance
        if instance and 'stage' in data and data['stage'] != instance.stage:
            if not instance.can_transition_to(data['stage']):
                raise serializers.ValidationError(
                    f"Invalid transition from {instance.stage} to {data['stage']}"
                )
        return data