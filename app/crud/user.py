from sqlalchemy.orm import Session

from app.models import User
from app import schemas
from app.core.utils import hash_password


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_create: schemas.UserCreate) -> User:
    # hash the password and create a new User instance:
    new_user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        password_hash=hash_password(user_create.password),
    )
    db.add(new_user)
    db.commit()
    # Refresh the instance to include database-generated fields:
    db.refresh(new_user)
    return new_user