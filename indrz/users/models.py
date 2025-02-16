from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.conf import settings
from django.urls import reverse

from organizations.models import Department

class CustomUserManager(BaseUserManager):
    """Manager for custom user model."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Username field must be set')

        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Replace AbstractUser with AbstractBaseUser + PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        (1, 'campus-admin'),
        (2, 'campus-user'),
        (3, 'bookway-admin'),
        (4, 'bookway-user'),
        (5, 'admin'),
        (6, 'webapp'),
    )

    # Required or custom fields for your user
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # Ext is external ids
    ext_person_id = models.IntegerField(unique=True, blank=True, null=True)
    ext_dept_ids = ArrayField(models.IntegerField(), default=list, blank=True)
    ext_dept_codes = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    username = models.CharField(max_length=150, unique=False)
    temp_saml_token = models.CharField(max_length=100, blank=True, null=True)

    user_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=USER_TYPE_CHOICES
    )

    # M2M to Department
    departments = models.ManyToManyField(Department, related_name='users', blank=True)

    # Basic Django-required permissions fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Associate with CustomUserManager
    objects = CustomUserManager()

    # `USERNAME_FIELD` tells Django which field is used to log in
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []   # If you want email, first_name, etc., add them here

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["email"]

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.email})


# Signal to create auth token on user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ExtUsers(models.Model):
    """
    A read-only model pointing to geodata.tu_user_departments.
    This matches the columns from your existing table.
    """
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    ext_person_id = models.IntegerField(unique=True)
    ext_dept_ids = ArrayField(models.IntegerField(), default=list, blank=True)
    ext_dept_codes = ArrayField(models.TextField(), default=list, blank=True)

    class Meta:
        managed = False  # Do not create or modify this table
        db_table = 'geodata"."ext_users'

    def __str__(self):
        return f"{self.email} ({self.ext_person_id})"


class ExtDepartment(models.Model):
    # id field is automatically connected by django
    name_en = models.TextField(null=True, blank=True)
    name_de = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    ext_dept_id = models.IntegerField(null=True, blank=True)
    ext_dept_code = models.CharField(max_length=50, null=True, blank=True)
    ext_parent_dept_code = models.CharField(max_length=50, null=True, blank=True)
    ext_parent_dept_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'geodata\".\"ext_departments'
        managed = False  # Tells Django not to manage this table
        app_label = 'users'  # Replace with your actual app name

    def __str__(self):
        return self.name_de or self.name_en or f"Department {self.id}"