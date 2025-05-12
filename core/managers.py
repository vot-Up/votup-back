from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Count

from core import models as core_models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, cellphone=None, **extra_fields):
        if not email:
            raise ValueError('O campo email precisa ser preenchido')
        if not cellphone:
            raise ValueError('O campo celular precisa ser preenchido')
        email = self.normalize_email(email)
        user = self.model(email=email, cellphone=cellphone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password, cellphone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email=email, password=password, cellphone=cellphone, **extra_fields)


class VotingUserManager(models.Manager):
    def ranking(self, voting_id: int):
        return self.get_queryset().values('plate__id', 'plate__name').annotate(
            total=Count('*')
        ).filter(voting_id=voting_id, voter__isnull=False, ).order_by('-total')
