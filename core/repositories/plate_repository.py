from core.domain.plate import Plate
from core.models import models
from core.ports.plate_repository_port import PlateRepositoryPort


class PlateRepository(PlateRepositoryPort):
    def get_conflicting_plate_ids(self, plate_id: int) -> list[int]:
        list_candidate = models.PlateUser.objects.filter(plate=plate_id).values('candidate_id')

        plate_list = models.PlateUser.objects.filter(
            candidate__in=list_candidate
        ).values_list('plate_id', flat=True).exclude(plate_id=plate_id)

        return list(plate_list)

    def get_by_id(self, plate_id: int) -> Plate:
        plate_obj = models.Plate.objects.get(id=plate_id)
        return Plate(
            id=plate_obj.id,
            name=plate_obj.name,
            was_voted=plate_obj.voting_user_plate.exists(),
            active=plate_obj.active
        )

    def save(self, plate: Plate) -> None:
        models.Plate.objects.filter(id=plate.id).update(active=plate.is_active)
