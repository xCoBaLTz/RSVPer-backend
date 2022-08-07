from pydantic import BaseModel


class Invite(BaseModel):
    id: str
    first_name: str
    last_name: str
    rsvp_status: bool
