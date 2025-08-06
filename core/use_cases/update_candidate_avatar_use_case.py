from core.ports.candidate_repository_port import CandidateRepositoryPort
from core.ports.file_storage_port import FileStoragePort

class UpdateCandidateAvatarUseCase:
    def __init__(self, storage: FileStoragePort, repository: CandidateRepositoryPort):
        self.storage = storage
        self.repository = repository


    def execute(self, candidate_id: int, file: bytes, filename: str):
        candidate = self.repository.get_by_id(candidate_id)

        if candidate.avatar_url:
            self.storage.delete(candidate.avatar_url)

        new_url = self.storage.upload(file, filename)
        candidate.avatar_url = new_url

        self.repository.save(candidate)