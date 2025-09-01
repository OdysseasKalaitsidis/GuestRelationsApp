import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse

# Create Base first (always needed)
Base = declarative_base()

# Initialize engine and SessionLocal as None
engine = None
SessionLocal = None

def get_database_url():
    """Get database URL from environment variables"""
    mysql_url = os.environ.get("MYSQL_URL")
    
    if mysql_url:
        # Parse MYSQL_URL if available
        parsed = urlparse(mysql_url)
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        port = parsed.port
        database = parsed.path.lstrip("/")  # VERY IMPORTANT - removes leading slash
        connection_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    else:
        # Fallback using separate Railway variables with proper stripping
        user = os.environ.get("MYSQLUSER", "").strip()
        password = os.environ.get("MYSQLPASSWORD", "").strip()
        host = os.environ.get("MYSQLHOST", "").strip()
        port = os.environ.get("MYSQLPORT", "3306")
        database = os.environ.get("DB_NAME", "").strip()
        
        # Check if all required environment variables are set
        if not all([user, password, host, database]):
            return None
            
        connection_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    
    return connection_url

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
