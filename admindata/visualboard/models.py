from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User  # 고민 


# Create your models here.
class DateTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Main DB initialization
class UserTire(models.Model):
    class UserTier(models.TextChoices):
        NORMALUSER = "일반유저"
        VIPUSER = "뿜뿜유저"

    username = models.CharField(max_length=30, primary_key=True, verbose_name="이름")
    tire = models.CharField(max_length=10, choices=UserTier.choices, default=UserTier.NORMALUSER)

    class Meta:
        db_table = "usertire"


class UserInformation(DateTimeStamp):
    username = models.CharField(max_length=30)
    nick_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    user_tire = models.ForeignKey(UserTire, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120, unique=True, verbose_name="이메일")

    class Meta:
        db_table = "userinfo"
        indexes = [
            models.Index(
                fields=(
                    "username",
                    "email"
                )
            )
        ]


# admin database
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password=password)
        user.save(using=self._db)

        return user


class AdminUsers(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="이름")
    is_active = models.BooleanField(default=True, verbose_name="활성화")
    email = models.EmailField(max_length=120, unique=True, verbose_name="이메일")
    USERNAME_FIELD: str = "email"

    # admin create setting --> UserManager
    object = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    # index
    class Meta:
        db_table = "adminUser"
        indexes = [
            models.Index(
                fields=[
                    "email",
                    "full_name",
                ]
            )
        ]
