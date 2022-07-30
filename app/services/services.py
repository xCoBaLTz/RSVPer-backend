import os
import jwt
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, security

from app import models, validator, database, schemas

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

oauth2schema = security.OAuth2PasswordBearer("/token")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: Session) -> models.User:
    return db.query(schemas.User).filter(schemas.User.email == email).first()


async def get_invites(user_id: UUID, db: Session) -> List[models.Invite]:
    return db.query(schemas.Invite).filter(schemas.Invite.user_id == user_id).all()


async def create_token(user: schemas.User):
    user_schema_obj = models.User(id=str(user.id), email=user.email)
    user_dict = user_schema_obj.dict()
    token = jwt.encode(user_dict, JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2schema)
):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    user = db.query(schemas.User).get(payload["id"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return models.User(id=str(user.id), email=user.email)


async def authenticate_user(email: str, db: Session):
    user = await get_user_by_email(email=validator.validate_email(email), db=db)
    if not user:
        return False
    return user
