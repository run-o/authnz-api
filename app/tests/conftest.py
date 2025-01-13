import pytest
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

from sqlalchemy import create_engine
from app.main import app
from app.db import get_db
from app.db.database import Base
from app.core.security import create_auth_token
from app.tests.utils.user import (
    get_or_create_user,
    create_user_data_for_email,
    get_login_authtoken,
)


# NOTE: we point to the test database by setting SQLALCHEMY_DB_USER_URI
# and SQLALCHEMY_DB_OWNER_URI in pyproject.toml

    
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    # create the test DB engine with owner role:
    owner_engine = create_engine("postgresql://authnz_owner:authnz_owner@localhost/authnz_test")
    try:
        # try dropping all tables in case they were not cleaned up properly:
        Base.metadata.drop_all(bind=owner_engine)
    except Exception:
        pass
    
    # Re-run all migrations for the test DB:
    # NOTE: we need to run the migrations on the test DB rather than just relying
    # on Base.metadata.create_all() because we need to set up the RLS policies 
    alembic_cfg = Config("alembic.ini")
    command.stamp(alembic_cfg, "base")
    command.upgrade(alembic_cfg, 'head')
    yield
    # Drop tables after tests:
    Base.metadata.drop_all(bind=owner_engine)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client
            
    
@pytest.fixture
def test_db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()
              
        
@pytest.fixture
def valid_jwt_token():
    token = create_auth_token({
        'user_id': 'some-uuid',
        'email': 'email@test.com'
    })
    return f"Bearer {token}"


@pytest.fixture
def logged_in_user_token_header(client, test_db):
    """ This fixture will log the given user in, creating the user if it
        doesn't exist and return the corresponding authtoken.
    """
    def authtoken(email: str):
        get_or_create_user(test_db, email)
        return get_login_authtoken(client, email)

    return authtoken


@pytest.fixture
def create_user(test_db):
    def create_user_for_email(email: str):
        return get_or_create_user(test_db, email)
        
    return create_user_for_email


@pytest.fixture
def create_user_data(test_db):
    def create_data_for_email(email: str, data: str):
        create_user_data_for_email(test_db, email, data)
        
    return create_data_for_email


