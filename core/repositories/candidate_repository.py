from core.domain.candidate import Candidate
from core.models import models
from core.ports.candidate_repository_port import CandidateRepositoryPort


class CandidateRepository(CandidateRepositoryPort):
    def get_by_id(self, candidate_id: int):
        candidate_obj = models.Candidate.objects.get(pk=candidate_id)
        return Candidate(
            id=candidate_obj.id,
            name=candidate_obj.name,
            cellphone=candidate_obj.cellphone,
            disable=candidate_obj.disabled
        )

    def save(self, candidate: Candidate):
        models.Candidate.objects.filter(id=candidate.id).update(disabled=candidate.disable)
