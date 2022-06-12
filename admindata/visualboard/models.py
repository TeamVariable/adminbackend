from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User  # 고민 

# Create your models here.

# admin database
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password=password)
        user.save(using=self._db)

        return user


class AdminUsers(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=120, unique=True, verbose_name="이메일")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD: str = "email"

    # admin create setting --> UserManager
    object = UserManager()

    @property
    def is_staff(self):
        return self.is_admin
    
    # index
    class Meta:
        app_label = "AdminUser"
        indexes = [
            models.Index(
                fields=[
                    "email",
                    "full_name"
                ]
            )
        ]
