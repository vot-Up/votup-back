"""
core/services/voter_service.py — Lógica de eleitores (migrada de use_cases/voter_use_case.py)

Substitui GetVoter + VoterRepository + VoterDTO.
Acessa modelos diretamente via core.models.models, sem Port/Repository intermediário.
"""

from core import exceptions
from core.models import models


def get_voter(cellphone: str) -> dict:
    """Retorna dados de um eleitor verificado pelo celular.

    Substitui GetVoter(repository=VoterRepository()).execute(cellphone)
    seguido de VoterDTO.model_validate(voter).model_dump().

    Args:
        cellphone: Número de celular do eleitor.

    Returns:
        dict com id, name, cellphone, has_voted.

    Raises:
        CellphoneDoesNotUserException: Se o eleitor não existir.
        Exception: Se o eleitor já votou ("Este eleitor já votou.").
    """
    try:
        voter_obj = models.Voter.objects.get(cellphone=cellphone)
    except models.Voter.DoesNotExist:
        raise exceptions.CellphoneDoesNotUserException()

    has_voted = bool(voter_obj.votinguser_set.filter(plate__isnull=False).exists())

    if has_voted:
        raise Exception("Este eleitor já votou.")

    return {
        "id": voter_obj.id,
        "name": voter_obj.name,
        "cellphone": voter_obj.cellphone,
        "has_voted": has_voted,
    }
