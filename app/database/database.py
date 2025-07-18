from sqlmodel import SQLModel, Session, create_engine 
from contextlib import contextmanager
from .config import get_settings
from models.user import User
from models.balance import Balance
from models.transaction import Transaction
from models.prediction import Prediction
from auth.hash_password import HashPassword
from services.crud.user import create_user, get_all_users, get_user_by_email
from services.crud.balance import create_balance
from services.crud.transaction import create_transaction
from services.crud.prediction import create_prediction

def get_database_engine():
    """
    Create and configure the SQLAlchemy engine.
    
    Returns:
        Engine: Configured SQLAlchemy engine
    """
    settings = get_settings()
    
    engine = create_engine(
        url=settings.DATABASE_URL_psycopg,
        echo=settings.DEBUG,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )
    return engine

engine = get_database_engine()

def get_session():
    with Session(engine) as session:
        yield session
        
def init_db(drop_all: bool = False) -> None:
    """
    Initialize database schema.
    
    Args:
        drop_all: If True, drops all tables before creation
    
    Raises:
        Exception: Any database-related exception
    """
    try:
        engine = get_database_engine()
        if drop_all:
            SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        paswd = HashPassword().create_hash('Qwerty123!')
        test_user = User(email='test1@gmail.com', password=paswd, name='Bob')
        admin = User(email='test1@gmail1.com', password=paswd, name='Alice', is_admin=True)
        with Session(engine) as session:
            check = get_user_by_email('test1@gmail.com', session)
            if not check:
                create_user(test_user, session)
                create_user(admin, session)
                balance1 = Balance(value=0, creator=test_user, user_id=test_user.id)
                balance2 = Balance(value=0, creator=admin, user_id=admin.id)
                create_balance(balance1, session)
                create_balance(balance2, session)
    except Exception as e:
        raise