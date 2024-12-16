import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app import schemas
from app import models
from app import crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/by_email', response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(get_db)) -> Any:
    """ Retrieve a user by email. """
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for email {email}."
        )
    return user


@router.post('/', response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new user. """
    # Check if email is already registered:
    existing_user = crud.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    try:
        new_user = crud.create_user(db, user_create)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    return new_user


@router.get("/me")
def get_authenticated_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    """ Example of a protected route. """
    return {"message": f"Welcome {current_user.first_name}!"}