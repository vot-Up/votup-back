from datetime import datetime

from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.db import transaction

from core import models, exceptions


class UserActions:
    @staticmethod
    @transaction.atomic
    def create_avatar(**kwargs):
        try:
            for item in kwargs.get('avatar'):
                avatar = models.User()
                avatar.avatar = ContentFile(name=item.name, content=item.read())
                avatar.file_name = item.name
                avatar.save()
        except ClientError:
            raise exceptions.MinioException()

    @staticmethod
    def reset_password(new_password: str, cellphone: str, email: str):
        try:
            valid_user = models.User.objects.get(cellphone=cellphone, email=email)
        except Exception:
            raise exceptions.UserNotExistException

        if new_password:
            valid_user.set_password(raw_password=new_password)
            valid_user.save()


class VotingPlateAction:
    @staticmethod
    def check_plate_voting(id_voting: int) -> bool:
        plate_id_to_check = models.VotingPlate.objects.filter(
            voting_id=id_voting
        ).values('plate_id')
        plates_associated = models.Plate.objects.filter(
            votingplate__voting=id_voting,
            id__in=plate_id_to_check
        )

        return plates_associated.values()

    @staticmethod
    def delete_voting_plate(voting: int, plate: int):
        try:
            models.VotingPlate.objects.filter(
                voting=voting,
                plate=plate
            ).delete()
        except Exception:
            raise exceptions.UnableRemovePlateException()


class EventVotingAction:
    @staticmethod
    def populate_resume_vote(id_plate: int, id_vote: int, quantity: int):
        event_voting = models.EventVoting.objects.get_or_create(id_vote=id_vote, id_plate=id_plate, quantity=quantity)
        if not event_voting:
            raise exceptions.EventVotingException()

    @staticmethod
    def delete_historic(event_vote: int):
        try:
            voting_users = models.VotingUser.objects.filter(voting_id=event_vote)

            for voting in voting_users:
                voting.delete()

            voting_plates = models.VotingPlate.objects.filter(voting_id=event_vote)

            for voting_plate in voting_plates:
                plate_users = models.PlateUser.objects.filter(plate_id=voting_plate.plate_id)
                plate_users.delete()
                voting_plate.delete()

            resume_votes = models.ResumeVote.objects.filter(voting_id=event_vote)

            for resume_vote in resume_votes:
                resume_vote.delete()

            events_voting = models.EventVoting.objects.filter(id=event_vote)
            events_voting.delete()

        except Exception:
            raise exceptions.ForeignKeyException


class VotingUserAction:
    @staticmethod
    def get_voting_user(cellphone: str):

        try:
            voter = models.Voter.objects.get(cellphone=cellphone)
        except Exception:
            raise exceptions.CellphoneDoesNotUserException()

        voting = models.EventVoting.objects.filter(active=True).first()

        if voting and models.VotingPlate.objects.filter(voting=voting).count() >= 2:
            if voting.date.date() < datetime.now().date():
                raise exceptions.TimeOverVotingException()

            voter = models.Voter.objects.get(id=voter.id)
            voting_user, _ = models.VotingUser.objects.get_or_create(voting=voting, voter=voter)

            if voting_user.plate:
                raise exceptions.UserHasAlreadyVotedException()

            return {
                'id': voting_user.id,
                'voting': voting_user.voting.id,
                'voter': voting_user.voter.id,
            }
        else:
            raise exceptions.NoActiveVotingException()

    @staticmethod
    def get_voter_plate(plate):
        plate_queryset = models.Voter.objects.filter(votinguser__plate=plate).values()
        return plate_queryset.values()


class VotingAction:

    @staticmethod
    def active_vote(vote_id: int):
        if models.EventVoting.objects.filter(active=True).count() > 0:
            raise exceptions.ExistVoteActiveException()

        vote = models.EventVoting.objects.filter(id=vote_id)
        vote.update(active=True)
        plates_votes = models.VotingPlate.objects.filter(voting_id=vote.first().id)
        if plates_votes:
            plate_ids = [i.plate_id for i in plates_votes]
            models.Plate.objects.filter(id__in=plate_ids).update(active=True)

    @staticmethod
    def close_vote(vote_id):
        vote = models.EventVoting.objects.filter(id=vote_id)
        vote.update(active=False)
        plates_votes = models.VotingPlate.objects.filter(voting_id=vote.first().id)
        if plates_votes:
            plate_ids = [i.plate_id for i in plates_votes]
            models.Plate.objects.filter(id__in=plate_ids).update(active=False)

    @staticmethod
    def get_pdf_user():
        return None


class PlateUserAction:

    @staticmethod
    def delete_user_plate(candidate: int, plate: int):
        try:
            models.PlateUser.objects.get(
                candidate=candidate,
                plate=plate
            ).delete()

            candidate_obj = models.Candidate.objects.get(pk=candidate)
            candidate_obj.disabled = False
            candidate_obj.save()

        except Exception:
            raise exceptions.UnableRemoveUserException()


class ResumeVoteAction:
    @staticmethod
    def get_resume_vote():
        return models.ResumeVote.objects.all().values()
