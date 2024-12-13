from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import verify_password, create_auth_token
from app.api.deps import unauthorized_exception
from app import crud

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """ Login user and return a JWT token. """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
       raise unauthorized_exception("Invalid credentials")

    auth_token = create_auth_token(data={
        'user_id': str(user.user_id),
        'email': user.email
    })
    
    return {"access_token": auth_token, "token_type": "bearer"}