from app import database
import app.schemas as schemas
import app.models as models
from sqlalchemy.orm import Session


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_token(email: str, db: Session) -> schemas.Token:
    return db.query(models.Token).filter(models.Token.email == email).first()
