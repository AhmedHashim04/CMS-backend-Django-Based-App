from rest_framework import serializers
from .models import PerformanceReview
from user.serializers import EmployeeSerializer
from user.models import Employee

class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = PerformanceReview
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    
class PerformanceReviewCreateSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        queryset=Employee.objects.all(),
        slug_field='slug'
    )
    class Meta:
        model = PerformanceReview
        fields = [
            'employee',
            'stage',
            'scheduled_date',
            'feedback',
            'reviewed_by',
            'approved_by',
        ]
        extra_kwargs = {
            'feedback': {'required': False, 'allow_null': True, 'allow_blank': True},
            'scheduled_date': {'required': False, 'allow_null': True},
            'reviewed_by': {'required': False, 'allow_null': True},
            'approved_by': {'required': False, 'allow_null': True},
        }


class PerformanceReviewTransitionSerializer(serializers.Serializer):
    stage = serializers.ChoiceField(choices=PerformanceReview.REVIEW_STAGES)
    feedback = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    reviewed_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    approved_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
