from typing import Protocol

from core.domain.voter import Voter


class VoterRepositoryPort(Protocol):
    def get_by_cellphone(self, cellphone: str) -> Voter:
        pass
