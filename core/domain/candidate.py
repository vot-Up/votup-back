class Candidate:
    def __init__(self, id: int, name: str, cellphone: str, disable: bool = False,avatar_url: str = None):
        self.id = id
        self.name = name
        self.cellphone = cellphone
        self._disabled = disable
        self.avatar_url = avatar_url

    def enable(self):
        self._disabled = False

    @property
    def disable(self):
        return self._disabled