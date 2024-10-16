from django.urls import path
from . import views
from .views import *

app_name = 'school'
urlpatterns = [
    path('register/', views.register_school, name='register_school'),
    path('email_sent/', views.email_sent, name='email_sent'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'), 
    path('authorize-student/<int:student_id>/', views.authorize_student, name='authorize_student'),
    path('admin/school/school/<int:school_id>/authorize/', authorize_school, name='authorize_school'),
    path('admin/school/school/<int:school_id>/deactivate/', deactivate_school, name='deactivate_school'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/profile/', views.profile_redirect_view, name='profile_redirect'),
    path('login/', school_login_view, name='login'),  # URL for login view
    path('dashboard/', school_dashboard, name='dashboard'),
]
