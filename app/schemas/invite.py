from datetime import datetime
from pydantic import BaseModel


class Invite(BaseModel):
    id: str
    user_id: str
    first_name: str
    last_name: str
    rsvp_status: bool
    created_at: datetime
    updated_at: datetime
