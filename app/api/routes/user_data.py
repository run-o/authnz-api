import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError

from app.db import get_db
from app.api.deps import AuthenticationRequired
from app import schemas
from app import crud

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user_data",
    tags=["User Data"],
    # all User Data routes require authentication:
    dependencies=[Depends(AuthenticationRequired)]
)


@router.get('/by_email', response_model=list[schemas.UserData], status_code=status.HTTP_200_OK)
def get_user_data(email: str, db: Session = Depends(get_db)) -> Any:
    """ Retrieve user data by email. """
    user_data = crud.get_user_data_by_email(db, email)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user data found for email {email}."
        )
    return user_data


@router.post('/', response_model=schemas.UserData)
def create_user_data(data_create: schemas.UserDataCreate, db: Session = Depends(get_db)) -> Any:
    """ Create new data for user. """
    try:
        new_data = crud.create_user_data(db, data_create)
    except ProgrammingError as exc:
        if "InsufficientPrivilege" in str(exc):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Cannot create data for user {data_create.user_id}.")
        else:
            raise
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    return new_data

