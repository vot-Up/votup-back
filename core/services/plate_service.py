"""
core/services/plate_service.py — Serviço de lógica de chapas/plates

Consolida o comportamento antes disperso em:
  - ActivatePlateUseCase
  - DeleteUserPlateUseCase
  - DeleteVotingPlateUseCase

Acessa os modelos diretamente via core.models.models,
sem Port/Repository intermediário.
"""

from django.db import transaction

from core import exceptions
from core.models import models


def activate_plate(plate_id: int):
    """Ativa uma chapa se nenhum de seus candidatos pertencer a outra chapa.

    Levanta PlateUserIsActiveException se algum candidato da chapa já
    estiver registrado em outra chapa.

    Args:
        plate_id: ID da chapa a ser ativada.

    Raises:
        DoesNotExist: Se a chapa não existir.
        PlateUserIsActiveException: Se houver candidatos compartilhados com outra chapa.
    """
    plate = models.Plate.objects.get(id=plate_id)

    candidate_ids = set(
        models.PlateUser.objects.filter(plate_id=plate_id).values_list("candidate_id", flat=True)
    )

    if not candidate_ids:
        plate.active = True
        plate.save(update_fields=["active"])
        return

    overlapping_plates = set(
        models.PlateUser.objects.filter(candidate_id__in=candidate_ids)
        .values_list("plate_id", flat=True)
        .distinct()
    )

    overlapping_plates.discard(plate_id)

    if overlapping_plates:
        raise exceptions.PlateUserIsActiveException()

    plate.active = True
    plate.save(update_fields=["active"])


def delete_user_plate(candidate_id: int, plate_id: int):
    """Remove um candidato de uma chapa e re-habilita o candidato.

    Args:
        candidate_id: ID do candidato a remover da chapa.
        plate_id: ID da chapa da qual remover o candidato.

    Raises:
        UnableRemovePlateException: Se a remoção falhar.
    """
    with transaction.atomic():
        try:
            models.PlateUser.objects.get(candidate=candidate_id, plate=plate_id).delete()
        except Exception:
            raise exceptions.UnableRemovePlateException()

        models.Candidate.objects.filter(pk=candidate_id).update(disabled=False)


def delete_voting_plate(voting: int, plate: int):
    """Remove a associação entre uma chapa e um evento de votação.

    Args:
        voting: ID do evento de votação.
        plate: ID da chapa.

    Raises:
        UnableRemovePlateException: Se a remoção falhar.
    """
    try:
        models.VotingPlate.objects.filter(voting=voting, plate=plate).delete()
    except Exception:
        raise exceptions.UnableRemovePlateException()
