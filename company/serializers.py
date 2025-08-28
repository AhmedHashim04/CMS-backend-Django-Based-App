from .models import Company, Department, Project
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    employee_count = serializers.SerializerMethodField()
    department_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    def get_employee_count(self, obj) -> int:
        return obj.employee_count 

    def get_department_count(self, obj) -> int:
        return obj.department_count

    def get_project_count(self, obj) -> int:
        return obj.project_count


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()
    def get_employee_count(self, obj) -> int:
        return obj.employee_count

    def get_project_count(self, obj) -> int:
        return obj.project_count

    class Meta:
        model = Department
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company'] = instance.company.name
        return representation


class ProjectSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Company.objects.all()
    )
    department = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Department.objects.all()
    )

    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company'] = instance.company.name
        representation['department'] = instance.department.name
        representation['assigned_employees'] = [employee.name for employee in instance.assigned_employees.all()]
        return representation
