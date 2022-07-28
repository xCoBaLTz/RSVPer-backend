import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import app.database as database


class User(database.Base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("token.id"))
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now)
