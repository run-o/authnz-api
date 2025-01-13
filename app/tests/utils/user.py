from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas


TEST_PASSWORD = 'test password'


def get_login_authtoken(client: TestClient, email: str):
    form_data = {"username": email, "password": TEST_PASSWORD}

    res = client.post(f"http://localhost:8000/login", data=form_data)
    response = res.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
    
def get_or_create_user(db: Session, email: str):
    user = crud.get_user_by_email(db=db, email=email)
    if not user:
        user_create = schemas.UserCreate(
            first_name="first_name",
            last_name="last_name",
            email=email,
            password=TEST_PASSWORD,
        )
        user = crud.create_user(db=db, user_create=user_create)
        
    return user

def create_user_data_for_email(db: Session, email: str, data: str):
    user = crud.get_user_by_email(db, email)
    db.set_actor_id(user.user_id)
    data_create = schemas.UserDataCreate(
        user_id=user.user_id,
        personal_data=data,
    )
    return crud.create_user_data(db, data_create)
