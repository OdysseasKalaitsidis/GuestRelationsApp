# Updated db.py for Supabase PostgreSQL

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

Base = declarative_base()
engine = None
SessionLocal = None
logger = logging.getLogger(__name__)

def get_database_url():
    """Build the SQLAlchemy database URL for Supabase"""
    return os.environ.get("DATABASE_URL")

def initialize_database():
    """Initialize engine and session with Supabase settings"""
    global engine, SessionLocal
    db_url = get_database_url()
    if db_url:
        logger.info("Initializing Supabase database connection")
        
        # Create async engine for Supabase PostgreSQL
        engine = create_async_engine(
            db_url,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=int(os.environ.get("DB_POOL_SIZE", 10)),
            max_overflow=int(os.environ.get("DB_MAX_OVERFLOW", 20))
        )
        
        # Create async session maker
        SessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        logger.info("Supabase database engine created successfully")
        return True
    else:
        logger.warning("No DATABASE_URL available")
        return False

async def get_db():
    """Provide an async database session"""
    if SessionLocal is None:
        if not initialize_database():
            raise RuntimeError("Database not configured. Check environment variables.")

    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_engine():
    """Get SQLAlchemy engine"""
    if engine is None:
        if not initialize_database():
            raise RuntimeError("Database not configured. Check environment variables.")
    return engine

async def test_connection():
    """Test database connection"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            logger.info(f"✅ Supabase test query returned: {value}")
            return True
    except Exception as e:
        logger.error(f"❌ Supabase connection test failed: {e}")
        return False

# Legacy MySQL support for rollback (optional)
def get_mysql_database_url():
    """Build the SQLAlchemy database URL for MySQL (for rollback)"""
    mysql_url = os.environ.get("LEGACY_MYSQL_URL")
    if mysql_url:
        if not mysql_url.startswith("mysql+pymysql://"):
            mysql_url = mysql_url.replace("mysql://", "mysql+pymysql://", 1)
        return mysql_url
    return None

def initialize_mysql_database():
    """Initialize MySQL engine for rollback scenarios"""
    global engine, SessionLocal
    db_url = get_mysql_database_url()
    if db_url:
        logger.info("Initializing MySQL database connection for rollback")
        
        # Add charset parameter
        if "?" in db_url:
            db_url += "&charset=utf8mb4"
        else:
            db_url += "?charset=utf8mb4"
        
        # Create sync engine for MySQL
        engine = create_engine(
            db_url,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
        SessionLocal = sessionmaker(bind=engine)
        
        logger.info("MySQL database engine created successfully for rollback")
        return True
    else:
        logger.warning("No LEGACY_MYSQL_URL available for rollback")
        return False
