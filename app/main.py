import logging
import jwt
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.database import engine, get_db, Base
from app import schemas
from app import models
from app import crud
from app.core.security import verify_password, create_auth_token, decode_auth_token


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# this will create the tables in postgres - move to Alembic later:
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ The lifespan startup context manager allows us to define code that
        should be executed before the application starts up and when the app
        is shutting down (potential cleanup steps).
    """
    yield
    # do cleanup here if necessary

app = FastAPI(lifespan=lifespan)

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
    user = None
    if not user:
        raise unauthorized_exception("User not found.")
    
    return user


@app.get('/')
async def root():
    return {"message": "Welcome to the FastAPI Authnz Sample Project: Access Control with Postgres RLS"}


@app.get('/users/by_email', response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(get_db)) -> models.User:
    """ Retrieve a user by email. """
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for email {email}."
        )

    return user


@app.post('/users', response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
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


@app.post("/login")
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


@app.get("/users/me")
def get_authenticated_user(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    """ Example of a protected route. """
    return {"message": f"Welcome {current_user.first_name}!"}