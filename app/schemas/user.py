from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    hostel_block: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    hostel_block: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str