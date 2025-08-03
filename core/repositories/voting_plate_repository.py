from core import exceptions
from core.models import models
from core.ports.voting_plate_repository_port import VotingPlateRepositoryPort


class VotingPlateRepository(VotingPlateRepositoryPort):
    def delete(self, voting: int, plate: int):
        try:
            models.VotingPlate.objects.filter(
                voting=voting,
                plate=plate
            ).delete()
        except Exception:
            raise exceptions.UnableRemovePlateException()

    def check_plate_associate(self, voting_id: int):
        plate_id_to_check = models.VotingPlate.objects.filter(
            voting_id=voting_id
        ).values('plate_id')
        plates_associated = models.Plate.objects.filter(
            votingplate__voting=voting_id,
            id__in=plate_id_to_check
        )

        return plates_associated.values()
