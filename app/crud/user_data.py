from typing import List
from sqlalchemy.orm import Session

from app.models import User, UserData
from app import schemas


def get_user_data_by_email(db: Session, email: str) -> List[UserData]:
    return db.query(UserData).join(User).filter(User.email == email).all()

def create_user_data(db: Session, data_create: schemas.UserDataCreate) -> UserData:
    new_data = UserData(
        user_id=data_create.user_id,
        personal_data=data_create.personal_data,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data