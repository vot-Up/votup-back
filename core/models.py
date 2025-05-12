from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from core import managers, messages
from django.contrib.postgres.fields import CITextField


def generate_filename(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = filename.split(".")[-1]
    new_filename = f"{timestamp}.{extension}"
    return new_filename


def upload_to(instance, filename):
    return f'media/{generate_filename(instance, filename)}'


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    cellphone = models.CharField(
        null=True,
        max_length=64,
        unique=True,
        error_messages={'unique': messages.CELLPHONE_ALREADY_EXISTS}
    )
    password = models.CharField(
        null=False,
        max_length=104,
    )
    name = models.CharField(
        null=True,
        max_length=256
    )
    email = models.EmailField(
        null=True,
        max_length=256,
        unique=True,
        error_messages={'unique': messages.EMAIL_ALREADY_EXISTS}
    )
    last_login = models.DateTimeField(
        null=True
    )
    is_superuser = models.BooleanField(
        null=True,
        default=False
    )
    is_staff = models.BooleanField(
        null=True,
        default=False
    )
    avatar = models.ImageField(
        upload_to=upload_to,
        null=True
    )
    file_name = models.CharField(null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=True,
    )
    is_active = models.BooleanField(
        null=False,
        default=True
    )

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cellphone', 'password']

    class Meta:
        db_table = 'user'
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
        default_permissions = ('add', 'change', 'delete', 'view')


class Voter(ModelBase):
    name = models.CharField(
        null=True,
        max_length=256
    )
    cellphone = models.CharField(
        null=True,
        max_length=64,
        unique=True,
        error_messages={'unique': messages.CELLPHONE_ALREADY_EXISTS}
    )
    avatar = models.ImageField(
        upload_to=upload_to,
        null=True
    )

    class Meta:
        db_table = 'voter'


class Candidate(ModelBase):
    name = models.CharField(
        null=True,
        max_length=256
    )
    cellphone = models.CharField(
        null=True,
        max_length=64,
        unique=True,
        error_messages={'unique': messages.CELLPHONE_ALREADY_EXISTS}
    )
    avatar = models.ImageField(
        upload_to=upload_to,
        null=True
    )
    disabled = models.BooleanField(
        default=False,
        db_column='disabled'
    )

    class Meta:
        db_table = 'candidate'


class Plate(ModelBase):
    name = models.CharField(
        null=False,
        unique=True,
        max_length=54,
        error_messages={'unique': messages.PLATE_ALREADY_EXISTS}
    )

    @property
    def was_voted(self):
        return VotingUser.objects.filter(plate=self.id).exists()

    class Meta:
        db_table = 'plate'


class PlateUser(ModelBase):
    candidate = models.ForeignKey(
        to=Candidate,
        on_delete=models.DO_NOTHING,
        db_column='id_candidate',
        related_name='candidate',
        null=True
    )
    plate = models.ForeignKey(
        to=Plate,
        on_delete=models.CASCADE,
        db_column='id_plate',
        related_name='plate',
        null=False
    )
    type = models.CharField(
        db_column="type",
        max_length=1,
        null=True,
    )

    class Meta:
        db_table = 'plate_user'
        unique_together = [
            ('plate', 'type')
        ]


class EventVoting(ModelBase):
    date = models.DateTimeField(
        null=True,
        verbose_name=('Date')
    )

    description = models.CharField(
        null=False,
        blank=False,
        max_length=54,
        verbose_name=('Description'),
        unique=True,
        error_messages={'unique': messages.VOTING_ALREADY_EXISTS}
    )

    @property
    def was_voted(self):
        return VotingUser.objects.filter(
            voting_id=self.id
        ).exists()

    class Meta:
        db_table = 'event_voting'


class VotingPlate(ModelBase):
    plate = models.ForeignKey(
        to=Plate,
        on_delete=models.DO_NOTHING,
        db_column='id_plate',
        null=False
    )

    voting = models.ForeignKey(
        to=EventVoting,
        on_delete=models.DO_NOTHING,
        db_column='id_voting',
        null=False
    )

    class Meta:
        db_table = 'voting_plate'
        unique_together = [
            ('voting', 'plate')
        ]


class VotingUser(ModelBase):
    voting = models.ForeignKey(
        to=EventVoting,
        on_delete=models.DO_NOTHING,
        db_column='id_voting',
        null=False
    )

    voter = models.ForeignKey(
        to=Voter,
        on_delete=models.DO_NOTHING,
        db_column='id_voter',
        null=True,
    )

    plate = models.ForeignKey(
        to=Plate,
        on_delete=models.DO_NOTHING,
        db_column='id_plate',
        related_name='voting_user_plate',
        null=True
    )

    objects = managers.VotingUserManager()

    class Meta:
        db_table = 'voting_user'
        unique_together = [
            ('voter', 'voting')
        ]


class ResumeVote(ModelBase):
    voting = models.ForeignKey(
        to=EventVoting,
        on_delete=models.DO_NOTHING,
        db_column='id_voting',
        null=True
    )
    plate = models.ForeignKey(
        to=Plate,
        on_delete=models.DO_NOTHING,
        db_column='id_plate',
        null=True
    )
    quantity = models.IntegerField(
        null=True,
        db_column='quantity_vote',
        default=0,
        blank=True
    )

    class Meta:
        db_table = 'resume_vote'
