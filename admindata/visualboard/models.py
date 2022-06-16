from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


# Create your models here.
class DateTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True


# Main DB initialization
class UserInformation(DateTimeStamp):
    username = models.CharField(max_length=30)
    nick_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=120, unique=True, verbose_name="이메일")

    class Meta:
        db_table: str = "userinfo"
        indexes = [
            models.Index(
                fields=(
                    "username",
                    "email"
                )
            )
        ]
        
class UserTire(models.Model):
    class UserTier(models.TextChoices):
        NORMALUSERL: str = "일반유저"
        VIPUSER: str = "뿜뿜유저"

    username = models.CharField(max_length=30, verbose_name="이름")
    tire = models.CharField(max_length=10, choices=UserTier.choices, default=UserTier.NORMALUSERL)
    info = models.ForeignKey(UserInformation, on_delete=models.CASCADE)

    class Meta:
        db_table: str = "usertire"


# admin database
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password=password)
        user.save(using=self._db)

        return user


class AdminUsers(AbstractBaseUser, PermissionsMixin, DateTimeStamp):
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
        db_table: str = "AdminUser"
        indexes = [
            models.Index(
                fields=[
                    "email",
                    "full_name",
                ]
            )
        ]
