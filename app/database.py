"""
Database configuration and connection management
"""
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database path from environment or use default
DATABASE_PATH = os.getenv("DATABASE_PATH", "expenses.db")

# Create database directory if it doesn't exist
db_path = Path(DATABASE_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

# Create database engine
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    """Create database tables if they don't exist"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session


def init_database():
    """Initialize the database"""
    create_db_and_tables()
    print(f"✓ Database initialized at: {DATABASE_PATH}")

