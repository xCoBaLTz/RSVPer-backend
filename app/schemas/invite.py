from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Invite(BaseModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    rsvp_status: bool
    created_at: datetime
    updated_at: datetime
