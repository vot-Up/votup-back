from pydantic import BaseModel


class VotingPlateDTO(BaseModel):
    id: int
    plate: int
    voting: int
