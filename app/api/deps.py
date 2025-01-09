import logging
import jwt
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.db import get_db
from app.core.security import decode_auth_token
from app import crud
from app.models import User

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

class UnauthorizedException(HTTPException):
    """ Construct an unauthorized exception that follows the OAuth2 spec. """
    def __init__(self, message="Invalid token."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail=message,
        )
        
class AuthenticatedContext:
    def __init__(self, db: Session, actor: str):
        self.db = db
        self.actor = actor
        self.actor_id = actor.user_id
    
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    """ Extract user information from the JWT token. """
    try:
        payload = decode_auth_token(token)
        email = payload.get('email')
        user_id = payload.get('user_id')
        if email is None or user_id is None:
            raise UnauthorizedException()
    except jwt.PyJWTError as exc:
        logger.info(f'Auth token failed validation: {str(exc)}')
        raise UnauthorizedException()
    
    # set the actor id at the DB level:
    db.set_actor_id(user_id) 
    
    user = crud.get_user_by_email(db, email)
    if not user:
        raise UnauthorizedException("User not found.")
    
    return user


def get_auth_context(
    db: Session = Depends(get_db),
    actor: str = Depends(get_current_user)
):
    return AuthenticatedContext(db=db, actor=actor)
    
class AuthenticationRequired:
    def __init__(
        self,
        user: User = Depends(get_current_user),
    ):
        pass