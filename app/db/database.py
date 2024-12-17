import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


engine = create_engine(
    # TODO: enable ssl in postgres and switch back to {'sslmode':'require'}
    settings.SQLALCHEMY_DB_URI, connect_args={'sslmode':'allow'}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def set_db_actor_id(db_session, user_id):
    logger.info(f"Setting db actor_id = {user_id} for session {db_session}")
    db_session.execute(text("SET LOCAL auth.actor_id = :user_id"), {"user_id": user_id})