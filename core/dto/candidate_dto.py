from pydantic import BaseModel


class CandidateDTO(BaseModel):
    id: int
    name: str
    cellphone: str
    disable: bool
    avatar_url: str | None = None
