from datetime import datetime, timedelta
import bcrypt
import jwt
from app.core.config import settings
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    """ Hashes a password using bcrypt. """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """ Verify a plain-text password against its hash. """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_auth_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """ Generate a JWT token. """
    payload = data.copy()
    payload.update({
        'exp': datetime.utcnow() + (expires_delta or timedelta(minutes=settings.AUTH_TOKEN_EXPIRE_MINUTES)),
        'iat': datetime.utcnow(),
    })
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

def decode_auth_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])