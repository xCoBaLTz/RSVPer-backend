import os
import jwt
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, security

from app import database, validator
import app.schemas as schemas
import app.models as models


JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

oauth2schema = security.OAuth2PasswordBearer("/token")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: Session) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


async def get_invites(user_id: UUID, db: Session) -> List[schemas.Invite]:
    return db.query(models.Invite).filter(models.Invite.user_id == user_id).all()


async def create_token(user: models.User):
    user_schema_obj = schemas.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    token = jwt.encode(user_dict, JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user = db.query(models.User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid Email")
    return schemas.User.from_orm(user)


async def authenticate_user(email: str, db: Session):
    user = await get_user_by_email(email=validator.validate_email(email), db=db)
    if not user:
        return False
    return user
