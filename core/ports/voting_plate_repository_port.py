from typing import Any, Protocol


class VotingPlateRepositoryPort(Protocol):
    def delete(self, voting_id: int, plate_id: int) -> None:
        pass

    def check_plate_associate(self, voting_id: int) -> list[dict[str, Any]]:
        pass
