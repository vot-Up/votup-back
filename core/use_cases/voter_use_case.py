from core.ports.voter_repository_ports import VoterRepositoryPort


class GetVoter:
    def __init__(self, repository: VoterRepositoryPort):
        self.repository = repository

    def execute(self, cellphone: str):
        voter = self.repository.get_by_cellphone(cellphone)
        voter.can_vote()
        return voter