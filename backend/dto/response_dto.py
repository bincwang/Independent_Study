from pydantic import BaseModel


class InfoResponse(BaseModel):
    username: str
    score: int
