from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class SchoolManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("The School must have an email address")
        if not username:
            raise ValueError("The School must have a username")

        school = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        school.set_password(password)
        school.save(using=self._db)
        return school

    def create_superuser(self, email, username, password=None):
        school = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        school.is_admin = True
        school.is_active = True
        school.is_verified = True
        school.save(using=self._db)
        return school

class School(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)  # For admin authorization
    is_verified = models.BooleanField(default=False)  # Email verification
    is_admin = models.BooleanField(default=False)  # Superuser status

    objects = SchoolManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        """This defines if the user is considered a staff member."""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Returns True if the user has a specific permission."""
        return True  # You can customize this based on your needs

    def has_module_perms(self, app_label):
        """Returns True if the user has permissions to view the app `app_label`."""
        return True  # You can customize this based on your needs
