from app.db.database import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    text,
    UUID,
)
from sqlalchemy.dialects.postgresql import UUID


class UserData(Base):
    __tablename__ = 'user_data'

    data_id = Column(UUID, primary_key=True, nullable=False,
                     server_default=text("uuid_generate_v4()"))
    personal_data = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey('users.user_id', ondelete='CASCADE'))

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))