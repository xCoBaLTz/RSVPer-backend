import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app import database as database


class User(database.base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String, index=True, unique=True)
