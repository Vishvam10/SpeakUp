from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    old_password: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: EmailStr