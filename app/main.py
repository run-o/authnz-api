import logging
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends, status
from app.db.database import engine, get_db, Base
from app import schemas
from app import models
from app import crud


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


@app.get('/')
async def root():
    return {"message": "Welcome to the FastAPI Authnz Sample Project: Access Control with Postgres RLS"}


@app.get('/users/by_email', response_model=schemas.User, status_code=status.HTTP_200_OK)
def get_user(email: str, db: Session = Depends(get_db)) -> models.User:
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found for email {email}."
        )

    return user


@app.post('/users', response_model=schemas.User)
def create_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered:
    existing_user = crud.get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    try:
        new_user = crud.create_user(db, user_create)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    return new_user