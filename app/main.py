import logging
import jwt
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.db.database import engine, get_db, Base
from app import schemas
from app import models
from app import crud
from app.core.utils import verify_password, create_auth_token, decode_auth_token


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Extract user information from the JWT token. """
    try:
        payload = decode_auth_token(token)
        email = payload.get('email')
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError as exc:
        logger.info(f'Auth token failed validation: {str(exc)}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
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
def login(email: str, password: str, db: Session = Depends(get_db)):
    """ Login user and return a JWT token. """

    user = crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    auth_token = create_auth_token(data={
        'user_id': str(user.user_id),
        'email': user.email
    })
    
    return {"auth_token": auth_token, "token_type": "bearer"}


@app.get("/protected")
def read_protected_data(current_user: models.User = Depends(get_current_user)):
    """ Example of a protected route. """
    return {"message": f"Welcome {current_user.first_name}!"}