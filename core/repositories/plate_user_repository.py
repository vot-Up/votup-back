from core import exceptions
from core.models import models
from core.ports.plate_user_repository_port import PlateUserRepositoryPort


class PlateUserRepository(PlateUserRepositoryPort):
    def delete(self, candidate: int, plate: int):
        try:
            models.PlateUser.objects.get(
                candidate=candidate,
                plate=plate
            ).delete()
        except Exception:
            raise exceptions.UnableRemovePlateException()
