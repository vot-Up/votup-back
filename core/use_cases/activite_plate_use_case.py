from core.ports.plate_repository_port import PlateRepositoryPort


class ActivatePlateUseCase:
    def __init__(self, repository: PlateRepositoryPort):
        self.repository = repository

    def execute(self, plate_id: int):
        conflicting_ids = self.repository.get_conflicting_plate_ids(plate_id)
        plate = self.repository.get_by_id(plate_id)

        plate.activate(conflicting_ids)

        self.repository.save(plate)
