import logging
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from app.core.config import settings

logger = logging.getLogger(__name__)

RLS_UNAUTHENTICATED_USER_ID = 'unauthenticated-user'


def _set_local_actor_id_var(connection, actor_id):
    """ Set a Postgres local variable using `SET LOCAL` so that it is only valid for
        the duration of the transaction and doesn't remain set across sessions.
    """
    logger.info(f"Setting Postgres local actor_id = {actor_id} for connection {connection}")
    # NOTE: we need to execute the command on the connection rather than the session
    # https://github.com/sqlalchemy/sqlalchemy/discussions/10469
    connection.execute(text("SET LOCAL auth.actor_id = :user_id"), {"user_id": str(actor_id)})


class SessionRLS(Session):
    """ Custom Session class for Postgres RLS that includes the user id
        of the currently authenticated user.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_id = RLS_UNAUTHENTICATED_USER_ID
        
    def set_actor_id(self, user_id):
        """ Set the session's actor_id and the corresponding Postgres local variable """
        self.actor_id = user_id
        _set_local_actor_id_var(self.connection(), self.actor_id)


engine = create_engine(
    # TODO: enable ssl in postgres and switch back to {'sslmode':'require'}
    settings.SQLALCHEMY_DB_USER_URI, connect_args={'sslmode':'allow'}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=SessionRLS)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    
@event.listens_for(SessionLocal, 'after_begin')
def after_begin_handler(db_session, transaction, connection): 
    """ Set the actor id at the beginning of each transaction by listening for the after_begin event.
    """
    _set_local_actor_id_var(connection, db_session.actor_id)
    

