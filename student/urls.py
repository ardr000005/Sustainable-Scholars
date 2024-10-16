from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('courses/', views.courses_view, name='courses'),
    path('goals/', views.goals_view, name='goals'),
    path('carbon/', views.carbon_view, name='carbon'),
    path('register/', views.register_student, name='register'),
    path('login/', views.student_login, name='student_login'),  # Ensure this line is correct
]
