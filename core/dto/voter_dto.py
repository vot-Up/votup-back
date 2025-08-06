from pydantic import BaseModel

class VoterDTO(BaseModel):
    id: int
    name: str
    cellphone: str
    has_voted: bool = False