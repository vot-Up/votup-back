from abc import ABC, abstractmethod


class ReportRepositoryPort(ABC):
    @abstractmethod
    def get_general_vote_result(self, event_vote_id: int) -> list[tuple[str, str, int]]:
        pass
