import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DB URI to be used for API connections (API user role):
    SQLALCHEMY_DB_USER_URI: str = (os.environ.get('SQLALCHEMY_DB_USER_URI') or
                                   "postgresql://authnz_user:authnz_user@localhost/authnz")
    # DB URI to be used for migrations (owner role):
    SQLALCHEMY_DB_OWNER_URI: str = (os.environ.get('SQLALCHEMY_DB_OWNER_URI') or
                                    "postgresql://authnz_owner:authnz_owner@localhost/authnz")
    
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY') or "some_secret_key"
    AUTH_TOKEN_EXPIRE_MINUTES: int = os.environ.get('AUTH_TOKEN_EXPIRE_MINUTES') or 30
    
    
settings = Settings()