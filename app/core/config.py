from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # TODO: read DB params from env variable:
    sqlalchemy_string: str = "postgresql://authnz_owner:authnz_owner@localhost/authnz"
    
settings = Settings()