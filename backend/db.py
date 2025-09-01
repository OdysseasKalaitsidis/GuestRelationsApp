import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create Base first (always needed)
Base = declarative_base()

# Initialize engine and SessionLocal as None
engine = None
SessionLocal = None

def get_database_url():
    """Get database URL from environment variables"""
    # Get MySQL environment variables with defaults
    DB_USER = os.getenv('MYSQLUSER')
    DB_PASSWORD = os.getenv('MYSQLPASSWORD')
    DB_HOST = os.getenv('MYSQLHOST')
    DB_PORT = os.getenv('MYSQLPORT', '3306')  # Default to 3306 if not set
    DB_NAME = os.getenv('DB_NAME')
    
    # Check if all required environment variables are set
    if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
        return None
    
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def initialize_database():
    """Initialize database connection if environment variables are available"""
    global engine, SessionLocal
    
    database_url = get_database_url()
    if database_url:
        engine = create_engine(database_url, echo=True)
        SessionLocal = sessionmaker(bind=engine)
        return True
    return False

def get_db():
    """Get database session"""
    if SessionLocal is None:
        # Try to initialize if not already done
        if not initialize_database():
            raise RuntimeError("Database not configured. Please check environment variables.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    """Get database engine"""
    if engine is None:
        # Try to initialize if not already done
        if not initialize_database():
            raise RuntimeError("Database not configured. Please check environment variables.")
    return engine
