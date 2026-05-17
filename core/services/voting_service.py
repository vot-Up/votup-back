"""
core/services/voting_service.py — Lógica de votação (migrada de use_cases/actions.py)

Substitui EventVotingAction, VotingAction, VotingUserAction, ResumeVoteAction.
Acessa modelos diretamente via core.models.models, sem Port/Repository intermediário.
"""

from datetime import datetime

from core import exceptions
from core.models import models


def delete_historic(event_vote: int):
    """Remove todo o histórico de um evento de votação.

    Deleta voting_users, voting_plates, plate_users, resume_votes e o próprio evento.

    Args:
        event_vote: ID do evento de votação.

    Raises:
        ForeignKeyException: Se a remoção falhar.
    """
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


def active_vote(vote_id: int):
    """Ativa um evento de votação e suas chapas associadas.

    Levanta ExistVoteActiveException se já houver uma votação ativa.

    Args:
        vote_id: ID do evento de votação a ativar.

    Raises:
        ExistVoteActiveException: Se já existir votação ativa.
    """
    if models.EventVoting.objects.filter(active=True).count() > 0:
        raise exceptions.ExistVoteActiveException()

    vote = models.EventVoting.objects.filter(id=vote_id)
    vote.update(active=True)

    plates_votes = models.VotingPlate.objects.filter(voting_id=vote.first().id)
    if plates_votes:
        plate_ids = [i.plate_id for i in plates_votes]
        models.Plate.objects.filter(id__in=plate_ids).update(active=True)


def close_vote(vote_id: int):
    """Encerra um evento de votação e desativa suas chapas associadas.

    Args:
        vote_id: ID do evento de votação a encerrar.
    """
    vote = models.EventVoting.objects.filter(id=vote_id)
    vote.update(active=False)

    plates_votes = models.VotingPlate.objects.filter(voting_id=vote.first().id)
    if plates_votes:
        plate_ids = [i.plate_id for i in plates_votes]
        models.Plate.objects.filter(id__in=plate_ids).update(active=False)


def get_voting_user(cellphone: str):
    """Retorna dados da votação atual para um eleitor.

    Args:
        cellphone: Número de celular do eleitor.

    Returns:
        dict com id, voting e voter.

    Raises:
        CellphoneDoesNotUserException: Se o eleitor não existir.
        TimeOverVotingException: Se a votação já encerrou.
        UserHasAlreadyVotedException: Se o eleitor já votou.
        NoActiveVotingException: Se não houver votação ativa.
    """
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
            "id": voting_user.id,
            "voting": voting_user.voting.id,
            "voter": voting_user.voter.id,
        }
    else:
        raise exceptions.NoActiveVotingException()


def get_voter_plate(plate):
    """Retorna eleitores associados a uma chapa.

    Args:
        plate: ID ou identificador da chapa.

    Returns:
        QuerySet de eleitores da chapa.
    """
    plate_queryset = models.Voter.objects.filter(votinguser__plate=plate).values()
    return plate_queryset.values()


def get_resume_vote():
    """Retorna todos os resumos de votação.

    Returns:
        QuerySet de ResumeVote.
    """
    return models.ResumeVote.objects.all().values()
