from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentRegistrationForm
from functools import wraps

# Student Registration View
def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=True)
            messages.success(request, 'Student registered successfully! Please log in.')
            return redirect('student:student_login')  # Redirect to login after successful registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'student/register.html', {'form': form})


# Student Login View
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Attempt to get the student by username
            student = Student.objects.get(username=username)
            if student.check_password(password):  # Verify password
                request.session['student_id'] = student.id  # Set session with student ID
                messages.success(request, 'Login successful!')
                return redirect('student:welcome')  # Redirect to the dashboard
            else:
                messages.error(request, 'Invalid password.')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid username.')

    return render(request, 'student/student_login.html')


# Student Logout View
def student_logout(request):
    try:
        del request.session['student_id']  # Clear session data
        messages.success(request, 'You have been logged out.')
    except KeyError:
        messages.error(request, 'You were not logged in.')
    return redirect('student_login')


# Decorator to ensure student is logged in
def student_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'student_id' not in request.session:
            return redirect('student_login')  # Redirect if student is not logged in
        return view_func(request, *args, **kwargs)
    return wrapper


# Student Dashboard View (requires login)
@student_login_required
def student_dashboard(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    return render(request, 'student/dashboard.html', {'student': student})


# Welcome View for logged-in students
@student_login_required
def welcome_view(request):
    student_id = request.session.get('student_id')
    student = Student.objects.get(id=student_id)
    return render(request, 'student/welcome.html', {'student': student})


# Additional views (courses, goals, carbon footprint)
@login_required(login_url='student:student_login')
def courses_view(request):
    # Example logic for courses view, customize as needed
    return render(request, 'student/courses.html')


@student_login_required
def goals_view(request):
    # Example logic for goals view, customize as needed
    return render(request, 'student/goals.html')


@student_login_required
def carbon_view(request):
    # Example logic for carbon view, customize as needed
    return render(request, 'student/carbon.html')
