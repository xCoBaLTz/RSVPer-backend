import fastapi
from sqlalchemy.orm import Session
from fastapi import FastAPI, Form, HTTPException
from app.services import services

app = FastAPI()


@app.post("/token")
async def login(email: str = Form(), db: Session = fastapi.Depends(services.get_db)):
    token = await services.get_token(email, db)
    return token if token else HTTPException(status_code=404, detail="User not found.")
