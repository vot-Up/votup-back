from core.ports.voting_plate_repository_port import VotingPlateRepositoryPort


class CheckPlateAssociateUseCase:
    def __init__(self, repository: VotingPlateRepositoryPort) -> None:
        self.repository = repository

    def execute(self, voting: int):
        return self.repository.check_plate_associate(voting)
