from uuid import UUID

from pydantic import BaseModel
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()


class User(BaseModel):
    id: UUID
    email: str


EMAILS: [User] = [
    User(id="639a42ec-1d3b-462e-9f8d-6efaff0dfe6e", email="seananchabra@hotmail.com")
]


@app.post("/login")
def login(email: str = Form()):
    for user in EMAILS:
        if email == user.email:
            return user
    return HTTPException(status_code=404, detail="User not found.")
