from pydantic import BaseModel


class Message(BaseModel):
    message: str

class User(BaseModel):
    username: str
    email: EmailStr
    password: str