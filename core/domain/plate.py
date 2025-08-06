from typing import List

from account import exceptions


class Plate:
    def __init__(self, id: int, name: str, was_voted: bool, active: bool = False):
        self.id = id
        self.name = name
        self._was_voted = was_voted
        self._active = active

    def activate(self, conflicting_plates: List[int]):
        if self.id in conflicting_plates:
            raise exceptions.PlateUserIsActiveException()
        self._active = True

    @property
    def is_active(self):
        return self._active

