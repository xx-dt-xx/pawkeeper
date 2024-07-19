from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Gender choices for users
GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('NB', 'Non-Binary'),
    )


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Must provide an email.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True)
    birthdate = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
