import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import app.database as database


class Token(database.Base):
    __tablename__ = "token"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String, index=True, unique=True)
