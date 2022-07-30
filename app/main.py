from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from uuid import UUID

from app.models import User, Invite
from app.services import services


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenRequest(BaseModel):
    email: str


@app.post("/token")
async def generate_token(request: TokenRequest, db: Session = Depends(services.get_db)):
    user = await services.authenticate_user(email=request.email, db=db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user=user)


@app.get("/users/me", response_model=User)
async def get_user(user: User = Depends(services.get_current_user)):
    return user


@app.get("/invites", response_model=List[Invite])
async def get_invites(user_id: UUID, db: Session = Depends(services.get_db)):
    invites = await services.get_invites(user_id, db)

    if not invites:
        raise HTTPException(status_code=404, detail="Invites not found")

    return invites
