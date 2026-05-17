"""
core/services/voting_plate_service.py — Serviço de lógica de associação VotingPlate

Consolida o comportamento antes em:
  - CheckPlateAssociateUseCase

Acessa os modelos diretamente via core.models.models,
sem Port/Repository intermediário.
"""

from core.models import models


def check_plate_associate(voting_id: int):
    """Retorna as chaps associadas a um evento de votação.

    Args:
        voting_id: ID do evento de votação.

    Returns:
        QuerySet de objetos Plate associados ao evento.
    """
    plate_id_to_check = models.VotingPlate.objects.filter(voting_id=voting_id).values("plate_id")
    plates_associated = models.Plate.objects.filter(
        votingplate__voting=voting_id, id__in=plate_id_to_check
    )

    return plates_associated.values()
