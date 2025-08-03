from pydantic import BaseModel


class PlateDTO(BaseModel):
    id: int
    name: str
