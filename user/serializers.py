from .models import Employee
from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # مهم عشان يتخزن مشفر
        user.save()
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Employee
        fields = ('slug', 'company', 'department', 'name', 'email', 'mobile', 'address', 'position', 'hired_on', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['get_days_employed'] = instance.get_days_employed
        representation['company'] = instance.company.name
        representation['department'] = instance.department.name
        return representation
