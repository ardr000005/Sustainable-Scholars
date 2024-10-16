# serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'school']

    def create(self, validated_data):
        # Hash the password before saving
        student = Student(**validated_data)
        student.set_password(validated_data['password'])  # Use the custom method to set the password
        student.save()
        return student

# serializers.py