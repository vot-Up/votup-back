from core.ports.candidate_repository_port import CandidateRepositoryPort
from core.ports.plate_user_repository_port import PlateUserRepositoryPort


class DeleteUserPlateUseCase:
    def __init__(
        self, plate_user_repository: PlateUserRepositoryPort, candidate_repository: CandidateRepositoryPort
    ) -> None:
        self.plate_user_repository = plate_user_repository
        self.candidate_repository = candidate_repository

    def execute(self, candidate_id: int, plate_id: int):
        self.plate_user_repository.delete(candidate_id, plate_id)

        candidate = self.candidate_repository.get_by_id(candidate_id)
        candidate.enable()
        self.candidate_repository.save(candidate)
