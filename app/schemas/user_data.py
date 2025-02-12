import uuid
from pydantic import AwareDatetime, BaseModel, ConfigDict


class UserDataBase(BaseModel):
    user_id: uuid.UUID
    personal_data: str

class UserDataCreate(UserDataBase):
    pass

class UserData(UserDataBase):
    data_id: uuid.UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime
    
    model_config = ConfigDict(from_attributes=True)