from typing import Optional

from pydantic import BaseModel


class Invite(BaseModel):
    id: str
    firstName: str
    lastName: str
    rsvpStatus: Optional[bool]
