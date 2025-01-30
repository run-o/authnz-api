from sqlalchemy.orm import Session

from app.models import User
from app import schemas
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_create: schemas.UserCreate) -> User:
    new_user = User(
        # get all fields from schema but exclude the password so we can hash it:
        **user_create.model_dump(exclude={"password"}),
        password_hash=hash_password(user_create.password),
    )
    db.add(new_user)
    db.commit()
    # Refresh the instance to include database-generated fields:
    db.refresh(new_user)
    return new_user