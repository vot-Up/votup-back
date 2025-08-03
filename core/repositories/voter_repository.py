from core.domain.voter import Voter as VoterDomain
from core.models.models import Voter
from core.ports.voter_repository_repository_port import VoterRepositoryPort


class VoterRepository(VoterRepositoryPort):
    def get_by_cellphone(self,cellphone: str) -> VoterDomain:
        voter_obj = Voter.objects.get(cellphone=cellphone)
        return VoterDomain(
            id=voter_obj.id,
            name=voter_obj.name,
            cellphone=voter_obj.cellphone,
            has_voted=bool(voter_obj.votinguser_set.filter(plate__isnull=False).exists())
        )