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
    MYSQLUSER = os.getenv('MYSQLUSER')
    MYSQLPASSWORD = os.getenv('MYSQLPASSWORD')
    MYSQLHOST = os.getenv('MYSQLHOST')
    MYSQLPORT = os.getenv('MYSQLPORT', '3306')  # Default to 3306 if not set
    MYSQLDATABASE = os.getenv('MYSQLDATABASE')
    
    # Check if all required environment variables are set
    if not all([MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE]):
        return None
    
    return (
        f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}"
        f"@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"
    )

def initialize_database():
    """Initialize database connection if environment variables are available"""
    global engine, SessionLocal
    
    database_url = get_database_url()
    if database_url:
        engine = create_engine(database_url, echo=False)
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
