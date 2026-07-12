from pydantic import BaseModel, EmailStr, Field


class RegisterForm(BaseModel):
    username: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    repeat_password: str = Field(min_length=8, max_length=128)


class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    preferred_language: str

    model_config = {"from_attributes": True}

