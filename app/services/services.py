import os
from datetime import datetime

import jwt
from typing import List, Union
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, security

from app import models, validator, database, schemas

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

oauth2schema = security.OAuth2PasswordBearer("/login")


def get_db():
    db = database.session()
    try:
        yield db
    finally:
        db.close()


async def get_invite_by_id(
    invite_id: UUID, user_id: UUID, db: Session
) -> models.Invite:
    return (
        db.query(schemas.Invite)
        .filter(schemas.Invite.id == invite_id)
        .filter(schemas.Invite.user_id == user_id)
        .first()
    )


async def get_user_by_email(email: str, db: Session) -> schemas.User:
    return db.query(schemas.User).filter(schemas.User.email == email).first()


async def get_invites(user_id: UUID, db: Session) -> List[models.Invite]:
    invites = (
        db.query(schemas.Invite)
        .filter(schemas.Invite.user_id == user_id)
        .order_by(schemas.Invite.first_name)
        .all()
    )
    return list(map(map_invite_schema_to_model, invites))


def map_invite_schema_to_model(invite: schemas.Invite) -> models.Invite:
    return models.Invite(
        id=str(invite.id),
        firstName=invite.first_name,
        lastName=invite.last_name,
        rsvpStatus=invite.rsvp_status,
    )


async def create_token(user: schemas.User) -> models.Auth:
    user_schema_obj = models.User(id=str(user.id), email=user.email)
    user_dict = user_schema_obj.dict()
    token = jwt.encode(user_dict, JWT_SECRET)

    return models.Auth(accessToken=token, tokenType="bearer")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2schema)
) -> models.User:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    user = db.query(schemas.User).get(payload["id"])
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials, please contact Seanan Chabra if you need assistance.",
        )
    return models.User(id=str(user.id), email=user.email)


async def authenticate_user(email: str, db: Session) -> Union[schemas.User, bool]:
    user: schemas.User = await get_user_by_email(
        email=validator.validate_email(email.lower()), db=db
    )
    if not user:
        return False
    return user


async def update_invite(
    invite_id: UUID, request: models.Invite, user_id: UUID, db: Session
) -> models.Invite:

    invite: schemas.Invite = await get_invite_by_id(
        invite_id=invite_id, user_id=user_id, db=db
    )

    if not invite:
        raise HTTPException(
            status_code=500,
            detail="Oops looks like something went wrong, please contact Seanan Chabra for further assistance.",
        )

    db.execute(
        text("UPDATE invites SET rsvp_status=:x, updated_at=:y WHERE id=:z"),
        {"x": request.rsvpStatus, "y": datetime.now(), "z": invite_id},
    )
    db.commit()
    db.refresh(invite)

    return models.Invite(
        id=str(invite.id),
        firstName=invite.first_name,
        lastName=invite.last_name,
        rsvpStatus=invite.rsvp_status,
    )
