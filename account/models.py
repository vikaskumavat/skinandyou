import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create User method called at user registration.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create superuser method called at superuser creation.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    GENDER_LIST = [('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.CharField(max_length=15)
    
    picture = models.ImageField(upload_to="profile", null=True, blank=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_LIST, max_length=8)
    
    highest_qualification = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    
    role = models.ForeignKey('core.UserRole',on_delete=models.PROTECT, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
            
    created_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name="created_user", null=True, blank=True)
    modified_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name="modified_user", null=True, blank=True)
    
    objects = UserManager()

    # Set email is a primary field which is used for login instead of username.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
    
    

class UserAddress(models.Model):
    # related_name="user_address_detail"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="user_address_detail", on_delete=models.PROTECT)
    address = models.TextField(max_length=300)
    landmark = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=50)
    city = models.ForeignKey("core.CityMaster", on_delete=models.PROTECT, null=True, blank=True)
    state = models.ForeignKey("core.StateMaster",on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "user_address"

    def __str__(self):
        return f"{self.user.email}, {self.address}"
