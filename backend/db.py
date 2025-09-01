import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse

Base = declarative_base()
engine = None
SessionLocal = None

def get_database_url():
    """Build the SQLAlchemy database URL"""
    mysql_url = os.environ.get("MYSQL_URL")

    if mysql_url:
        # Parse MYSQL_URL if available
        parsed = urlparse(mysql_url)
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        port = parsed.port
        database = parsed.path.lstrip("/")  # Remove leading slash
    else:
        # Fallback to separate variables
        user = os.environ.get("MYSQLUSER", "").strip()
        password = os.environ.get("MYSQLPASSWORD", "").strip()
        host = os.environ.get("MYSQLHOST", "").strip()
        port = os.environ.get("MYSQLPORT", "3306")
        database = os.environ.get("DB_NAME", "").strip()

        # If any required variable is missing, return None
        if not all([user, password, host, database]):
            return None

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

def initialize_database():
    """Initialize engine and session"""
    global engine, SessionLocal
    db_url = get_database_url()
    if db_url:
        engine = create_engine(db_url, echo=True)
        SessionLocal = sessionmaker(bind=engine)
        return True
    return False

def get_db():
    """Provide a database session"""
    if SessionLocal is None:
        if not initialize_database():
            raise RuntimeError("Database not configured. Check environment variables.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    """Get SQLAlchemy engine"""
    if engine is None:
        if not initialize_database():
            raise RuntimeError("Database not configured. Check environment variables.")
    return engine
