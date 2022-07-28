from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    id: UUID
    email: str
