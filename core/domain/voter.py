class Voter:
    def __init__(self, id: int, name: str, cellphone: str, has_voted: bool):
        self.id = id
        self.name = name
        self.cellphone = cellphone
        self._has_voted = has_voted

    def can_vote(self):
        if self._has_voted:
            raise Exception("Este eleitor já votou.")
        return True
