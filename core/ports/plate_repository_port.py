from typing import Protocol

from core.domain.plate import Plate


class PlateRepositoryPort(Protocol):
    def get_by_id(self, plate_id: int) -> Plate:
        pass

    def get_conflicting_plate_ids(self, plate_id: int) -> list[int]:
        pass

    def save(self, plate: Plate) -> None:
        pass
