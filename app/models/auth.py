from pydantic import BaseModel


class Auth(BaseModel):
    access_token: str
    token_type: str
