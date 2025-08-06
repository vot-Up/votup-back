from abc import ABC, abstractmethod
from typing import List, Tuple


class ReportRepositoryPort(ABC):
    @abstractmethod
    def get_general_vote_result(self, event_vote_id: int) -> List[Tuple[str, str, int]]:
        pass