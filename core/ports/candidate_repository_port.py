from typing import Protocol

from core.domain.candidate import Candidate


class CandidateRepositoryPort(Protocol):
    def get_by_id(self, candidate_id: int):
        pass

    def save(self, candidate: Candidate):
        pass
