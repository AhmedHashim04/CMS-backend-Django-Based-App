from .models import Company, Department, Project
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department_count'] = instance.department_count
        representation['employee_count'] = instance.employees.count
        representation['project_count'] = instance.project_count

        return representation

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee_count'] = instance.employees.count
        representation['project_count'] = instance.project_count
        return representation


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

