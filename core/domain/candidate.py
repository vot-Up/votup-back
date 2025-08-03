class Candidate:
    def __init__(self, id: int, name: str, cellphone: str, disable: bool = False):
        self.id = id
        self.name = name
        self.cellphone = cellphone
        self._disabled = disable

    def enable(self):
        self._disabled = False

    @property
    def disable(self):
        return self._disabled