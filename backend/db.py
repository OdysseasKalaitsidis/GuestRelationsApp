import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import urlparse

Base = declarative_base()
engine = None
SessionLocal = None
logger = logging.getLogger(__name__)

def get_database_url():
    """Build the SQLAlchemy database URL"""
    mysql_url = os.environ.get("MYSQL_URL")

    if mysql_url:
        # Use MYSQL_URL directly with Railway-specific parameters
        return mysql_url
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
    """Initialize engine and session with Railway-optimized settings"""
    global engine, SessionLocal
    db_url = get_database_url()
    if db_url:
        logger.info("Initializing database connection with Railway-optimized settings")
        # Railway MySQL connection configuration
        # Add charset and other Railway-specific parameters
        if "?" in db_url:
            db_url += "&charset=utf8mb4"
        else:
            db_url += "?charset=utf8mb4"
        
        logger.info(f"Database URL (with charset): {db_url.split('@')[0]}@***")
        
        # SSL configuration - Railway typically requires SSL but we'll try different approaches
        connect_args = {
            "charset": "utf8mb4"
        }
        
        # First try without SSL to see if that's the issue
        try_ssl = os.environ.get("MYSQL_REQUIRE_SSL", "true").lower() == "true"
        
        if try_ssl:
            ssl_ca_paths = [
                "/etc/ssl/certs/ca-certificates.crt",
                "/etc/ssl/certs/ca-bundle.crt", 
                "/usr/local/share/certs/ca-root-nss.crt"
            ]
            
            # Try to find a valid SSL CA certificate
            ssl_ca_found = None
            for ssl_ca_path in ssl_ca_paths:
                if os.path.exists(ssl_ca_path):
                    ssl_ca_found = ssl_ca_path
                    break
            
            if ssl_ca_found:
                connect_args["ssl"] = {"ssl_ca": ssl_ca_found}
                logger.info(f"Using SSL with CA certificate: {ssl_ca_found}")
            else:
                # Try basic SSL without specific CA
                connect_args["ssl"] = {"ssl_mode": "REQUIRED"}
                logger.info("Using SSL with required mode (no specific CA)")
        else:
            logger.info("SSL disabled via MYSQL_REQUIRE_SSL=false")
        
        # Create engine with Railway-specific settings
        engine = create_engine(
            db_url,
            echo=True,
            pool_pre_ping=True,  # Helps handle temporary disconnects
            pool_recycle=3600,   # Recycle connections every hour
            pool_size=10,        # Connection pool size
            max_overflow=20,     # Max overflow connections
            connect_args=connect_args
        )
        SessionLocal = sessionmaker(bind=engine)
        logger.info("Database engine created successfully with Railway settings")
        return True
    else:
        logger.warning("No database URL available - database features will be unavailable")
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
