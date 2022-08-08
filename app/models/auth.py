from pydantic import BaseModel


class Auth(BaseModel):
    accessToken: str
    tokenType: str
