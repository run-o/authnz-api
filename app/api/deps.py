import logging
import jwt
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db
from app.core.security import decode_auth_token
from app import crud

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def unauthorized_exception(message="Invalid token."):
    """ Construct an unauthorized exception that follows the OAuth2 spec. """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """ Extract user information from the JWT token. """
    try:
        payload = decode_auth_token(token)
        email = payload.get('email')
        if email is None:
            raise unauthorized_exception()
    except jwt.PyJWTError as exc:
        logger.info(f'Auth token failed validation: {str(exc)}')
        raise unauthorized_exception()
    
    user = crud.get_user_by_email(db, email)
    if not user:
        raise unauthorized_exception("User not found.")
    
    return user