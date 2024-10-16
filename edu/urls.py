from django.contrib import admin
from django.urls import path, include  # Include is needed to include app URLs
from django.contrib.auth import views as auth_views
from school import views as school_views  # Import views from school app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', school_views.login_selection, name='login_selection'),
    path('school/', include('school.urls')),
    path('student/', include(('student.urls', 'student'), namespace='student')),  
  # Include school app URLs here
]
