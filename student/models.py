# student/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):  # Inherit from AbstractUser
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_authorized = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)  # Make first_name optional
    last_name = models.CharField(max_length=30, blank=True, null=True)   # Make last_name optional

    def __str__(self):
        return self.username
