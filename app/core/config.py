import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DB URI to be used for API connections (API user role):
    SQLALCHEMY_DB_USER_URI: str = os.getenv('SQLALCHEMY_DB_USER_URI',
                                            "postgresql://authnz_user:authnz_user@localhost/authnz")
    # DB URI to be used for migrations (owner role):
    SQLALCHEMY_DB_OWNER_URI: str = os.getenv('SQLALCHEMY_DB_OWNER_URI',
                                             "postgresql://authnz_owner:authnz_owner@localhost/authnz")
    # Test DB URIs:
    SQLALCHEMY_TEST_DB_USER_URI: str = "postgresql://authnz_user:authnz_user@localhost/authnz_test"
    SQLALCHEMY_TEST_DB_OWNER_URI: str = "postgresql://authnz_owner:authnz_owner@localhost/authnz_test"
    
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', "some_secret_key")
    AUTH_TOKEN_EXPIRE_MINUTES: int = os.getenv('AUTH_TOKEN_EXPIRE_MINUTES', 30)
    
    
settings = Settings()