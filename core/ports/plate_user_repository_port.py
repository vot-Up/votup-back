from typing import Protocol, List, Any


class PlateUserRepositoryPort(Protocol):
    def delete(self, candidate_id: int, plate_id: int) -> None:
        pass