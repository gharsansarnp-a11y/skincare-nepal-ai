"""
Database Configuration

Handles PostgreSQL connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from .env, fallback to SQLite for MVP
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./skincare_nepal.db"  # SQLite database file in project root
)

# Create database engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't need pooling
    from sqlalchemy import create_engine as create_sqlite_engine
    engine = create_sqlite_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL with connection pooling
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        poolclass=NullPool if "localhost" in DATABASE_URL else None
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI endpoints
def get_db():
    """
    Dependency injection for database session.

    Usage in endpoints:
    @app.get("/api/endpoint")
    def my_endpoint(db: Session = Depends(get_db)):
        # Use db to query or save data
        pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check function
def test_db_connection():
    """
    Test if database connection works
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
