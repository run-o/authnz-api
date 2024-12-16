import uuid
from pydantic import BaseModel, AwareDatetime, EmailStr
from typing import Optional


class UserDataBase(BaseModel):
    user_id: uuid.UUID
    personal_data: str

class UserDataCreate(UserDataBase):
    pass

class UserData(UserDataBase):
    data_id: uuid.UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime
        