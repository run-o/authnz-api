from app.db.database import Base
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    text,
    UUID,
)
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID, primary_key=True, nullable=False,
                     server_default=text("uuid_generate_v4()"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    