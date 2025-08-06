from core.ports.voting_plate_repository_port import VotingPlateRepositoryPort


class DeleteVotingPlateUseCase:
    def __init__(self, repository: VotingPlateRepositoryPort) -> None:
        self.repository = repository

    def execute(self, voting: int, plate: int):
        self.repository.delete(voting, plate)
