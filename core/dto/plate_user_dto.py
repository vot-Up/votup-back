from pydantic import BaseModel


class PlateUserDTO(BaseModel):
    id: int
    candidate: int
    plate: int
    type: str
