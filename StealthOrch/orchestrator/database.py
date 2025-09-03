from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .config import settings

DATABASE_URL = settings.DB_PATH

# The connect_args is needed only for SQLite to allow multi-threaded access
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Creates the database and all tables defined in the models.
    """
    print("Creating database and tables...")
    Base.metadata.create_all(bind=engine)
    print("Database and tables created successfully.")

def get_db():
    """
    Dependency for FastAPI to get a DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
