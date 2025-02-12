import uuid
from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr
from typing import Optional


# Check this post for explanation about ORM model and pydantic schema:
# https://stackoverflow.com/questions/73700879/interaction-between-pydantic-models-schemas-in-the-fastapi-tutorial

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: uuid.UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime
    
    model_config = ConfigDict(from_attributes=True)
        