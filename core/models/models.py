from datetime import datetime

from django.db import models

from account import models as account_models
from core import managers, messages


def generate_filename(instance, filename):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    extension = filename.split(".")[-1]
    new_filename = f"{timestamp}.{extension}"
    return new_filename


def upload_to(instance, filename):
    return f"media/{generate_filename(instance, filename)}"


class Voter(account_models.ModelBase):
    name = models.CharField(null=True, max_length=256)
    cellphone = models.CharField(
        null=True, max_length=64, unique=True, error_messages={"unique": messages.CELLPHONE_ALREADY_EXISTS}
    )
    avatar = models.ImageField(upload_to=upload_to, null=True)

    class Meta:
        db_table = "voter"


class Candidate(account_models.ModelBase):
    name = models.CharField(null=True, max_length=256)
    cellphone = models.CharField(
        null=True, max_length=64, unique=True, error_messages={"unique": messages.CELLPHONE_ALREADY_EXISTS}
    )
    avatar_url = models.CharField(max_length=512, null=True, blank=True)

    disabled = models.BooleanField(default=False, db_column="disabled")

    class Meta:
        db_table = "candidate"


class Plate(account_models.ModelBase):
    name = models.CharField(
        null=False, unique=True, max_length=54, error_messages={"unique": messages.PLATE_ALREADY_EXISTS}
    )

    @property
    def was_voted(self):
        return VotingUser.objects.filter(plate=self.id).exists()

    class Meta:
        db_table = "plate"


class PlateUser(account_models.ModelBase):
    candidate = models.ForeignKey(
        to=Candidate, on_delete=models.DO_NOTHING, db_column="id_candidate", related_name="candidate", null=True
    )
    plate = models.ForeignKey(
        to=Plate, on_delete=models.CASCADE, db_column="id_plate", related_name="plate", null=False
    )
    type = models.CharField(
        db_column="type",
        max_length=1,
        null=True,
    )

    class Meta:
        db_table = "plate_user"
        unique_together = [("plate", "type")]


class EventVoting(account_models.ModelBase):
    date = models.DateTimeField(null=True, verbose_name=("Date"))

    description = models.CharField(
        null=False,
        blank=False,
        max_length=54,
        verbose_name=("Description"),
        unique=True,
        error_messages={"unique": messages.VOTING_ALREADY_EXISTS},
    )

    @property
    def was_voted(self):
        return VotingUser.objects.filter(voting_id=self.id).exists()

    class Meta:
        db_table = "event_voting"


class VotingPlate(account_models.ModelBase):
    plate = models.ForeignKey(to=Plate, on_delete=models.DO_NOTHING, db_column="id_plate", null=False)

    voting = models.ForeignKey(to=EventVoting, on_delete=models.DO_NOTHING, db_column="id_voting", null=False)

    class Meta:
        db_table = "voting_plate"
        unique_together = [("voting", "plate")]


class VotingUser(account_models.ModelBase):
    voting = models.ForeignKey(to=EventVoting, on_delete=models.DO_NOTHING, db_column="id_voting", null=False)

    voter = models.ForeignKey(
        to=Voter,
        on_delete=models.DO_NOTHING,
        db_column="id_voter",
        null=True,
    )

    plate = models.ForeignKey(
        to=Plate, on_delete=models.DO_NOTHING, db_column="id_plate", related_name="voting_user_plate", null=True
    )

    objects = managers.VotingUserManager()

    class Meta:
        db_table = "voting_user"
        unique_together = [("voter", "voting")]


class ResumeVote(account_models.ModelBase):
    voting = models.ForeignKey(to=EventVoting, on_delete=models.DO_NOTHING, db_column="id_voting", null=True)
    plate = models.ForeignKey(to=Plate, on_delete=models.DO_NOTHING, db_column="id_plate", null=True)
    quantity = models.IntegerField(null=True, db_column="quantity_vote", default=0, blank=True)

    class Meta:
        db_table = "resume_vote"
