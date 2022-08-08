from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from typing import List
from uuid import UUID

from app.models import User, Invite, Auth
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


@app.post("/token", response_model=Auth)
async def generate_token(
    request: TokenRequest, db: Session = Depends(services.get_db)
) -> Auth:
    user = await services.authenticate_user(email=request.email, db=db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials, please contact Seanan Chabra if you need assistance.",
        )

    return await services.create_token(user=user)


@app.get("/invites", response_model=List[Invite])
async def get_invites(
    user: User = Depends(services.get_current_user),
    db: Session = Depends(services.get_db),
) -> List[Invite]:
    invites = await services.get_invites(UUID(user.id), db)

    if not invites:
        raise HTTPException(
            status_code=404,
            detail="Invites not found, please contact Seanan Chabra if you need assistance.",
        )

    return invites


@app.put("/invites/{invite_id}", response_model=Invite)
async def update_invite(
    invite_id: str,
    request: Invite,
    user: User = Depends(services.get_current_user),
    db: Session = Depends(services.get_db),
) -> Invite:
    if invite_id != request.id:
        raise HTTPException(
            status_code=400,
            detail="Please make sure the request id matches the path parameter id",
        )

    invite = await services.update_invite(UUID(invite_id), request, UUID(user.id), db)

    if not invite:
        raise HTTPException(
            status_code=404,
            detail="Invites not found, please contact Seanan Chabra if you need assistance.",
        )

    return invite
