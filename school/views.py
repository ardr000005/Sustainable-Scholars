from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SchoolRegistrationForm
from .models import School
from student.models import Student


def register_school(request):
    """
    Handles school registration and sends an email for verification.
    """
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.is_active = False  # School needs to be activated by admin
            school.is_verified = False  # Email verification required
            school.save()

            # Generate email verification token and link
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(school.pk))
            token = default_token_generator.make_token(school)
            verification_link = f"http://{domain}/school/verify-email/{uid}/{token}/"

            # Send the verification email
            try:
                subject = 'Verify your school account'
                message = f'Please click the link to verify your account: {verification_link}'
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [school.email],
                    fail_silently=False,
                )
                messages.success(request, 'Please check your email to verify your account.')
                return redirect('school:email_sent')  # Redirect to email sent page
            except Exception as e:
                messages.error(request, 'There was an error sending the verification email. Please try again.')
                school.delete()  # Delete the school entry if email sending fails
    else:
        form = SchoolRegistrationForm()
    
    return render(request, 'school/register.html', {'form': form})


def verify_email(request, uidb64, token):
    """
    Handles email verification of a school account.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        school = get_object_or_404(School, pk=uid)
    except (TypeError, ValueError, OverflowError, School.DoesNotExist):
        school = None

    if school is not None and default_token_generator.check_token(school, token):
        school.is_verified = True
        school.save()
        messages.success(request, 'Your email has been verified successfully. Please wait for admin approval.')
        return redirect('school:login')  # Redirect to login page after verification
    else:
        messages.error(request, 'Email verification failed. The link is invalid.')
        return redirect('school:register_school')  # Redirect back to registration if verification fails


def custom_login_view(request):
    """
    Custom login view for school users.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('school_dashboard')  # Redirect to school dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'school/login.html')


@login_required
def school_dashboard(request):
    """
    Displays the dashboard with a list of students for the logged-in school.
    """
    students = Student.objects.filter(school=request.user)  # Assuming the school is the user
    return render(request, 'school/dashboard.html', {'students': students})


@login_required
def profile_view(request):
    """
    Displays the profile of the logged-in school.
    """
    school = request.user  # Assuming `request.user` is the logged-in School
    return render(request, 'school/profile.html', {'school': school})


def authorize_student(request, student_id):
    """
    Activates a student account under the current school.
    """
    student = get_object_or_404(Student, pk=student_id, school=request.user)
    student.is_active = True
    student.save()
    return redirect('school:school_dashboard')


def authorize_school(request, school_id):
    """
    Admin view to activate a school account.
    """
    school = get_object_or_404(School, id=school_id)
    school.is_active = True
    school.save()
    return redirect('/admin/school/school/')  # Redirect to the admin panel


def deactivate_school(request, school_id):
    """
    Admin view to deactivate a school account.
    """
    school = get_object_or_404(School, id=school_id)
    school.is_active = False
    school.save()
    return redirect('/admin/school/school/')  # Redirect to the admin panel


def email_sent(request):
    """
    Displays the confirmation page after the verification email is sent.
    """
    return render(request, 'school/email_sent.html')


def profile_redirect_view(request):
    """
    Redirects the user to their profile page.
    """
    return redirect('school:profile')


def school_login_view(request):
    """
    Handles school login.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('school:dashboard')  # Redirect to school dashboard
            else:
                messages.error(request, 'Your account is not active. Please contact admin.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'school/login.html')

from django.shortcuts import render, redirect

def login_selection(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type == 'admin':
            return redirect('/admin')
        elif user_type == 'school':
            return redirect('/school/login')
        elif user_type == 'student':
            return redirect('/student/login')
    return render(request, 'school/login_selection.html')  # Update the template path here
