from typing import Protocol, List, Any


class VotingPlateRepositoryPort(Protocol):
    def delete(self, voting_id: int, plate_id: int) -> None:
        pass

    def check_plate_associate(self, voting_id: int) -> List[dict[str, Any]]:
        pass