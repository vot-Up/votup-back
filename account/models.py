from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from account import managers, messages


def generate_filename(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = filename.split(".")[-1]
    new_filename = f"{timestamp}.{extension}"
    return new_filename


def upload_to(instance, filename):
    return f"media/{generate_filename(instance, filename)}"


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    cellphone = models.CharField(
        null=True, max_length=64, unique=True, error_messages={"unique": messages.CELLPHONE_ALREADY_EXISTS}
    )
    password = models.CharField(
        null=False,
        max_length=104,
    )
    name = models.CharField(null=True, max_length=256)
    email = models.EmailField(
        null=True, max_length=256, unique=True, error_messages={"unique": messages.EMAIL_ALREADY_EXISTS}
    )
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(null=True, default=False)
    is_staff = models.BooleanField(null=True, default=False)
    avatar = models.ImageField(upload_to=upload_to, null=True)
    file_name = models.CharField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    is_active = models.BooleanField(null=False, default=True)

    objects = managers.UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "cellphone", "password"]

    class Meta:
        db_table = "user"
        managed = True


class ModelBase(models.Model):
    id = models.BigAutoField(
        null=False,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    active = models.BooleanField(
        null=True,
        default=True,
    )

    class Meta:
        abstract = True
        managed = True
        default_permissions = ("add", "change", "delete", "view")
