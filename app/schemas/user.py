from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    token_id: UUID
    first_name: str
    last_name: str
    rsvp_status: bool
    created_at: datetime
    updated_at: datetime
