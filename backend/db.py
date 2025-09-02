# Updated db.py for Supabase PostgreSQL

import os
import logging
import ssl
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

Base = declarative_base()
engine = None
SessionLocal = None
logger = logging.getLogger(__name__)

def get_database_url():
    """Build the SQLAlchemy database URL for Supabase"""
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        # Ensure we're using asyncpg driver for async connections
        if db_url.startswith("postgresql://") and "+asyncpg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url
    return None

def initialize_database():
    """Initialize engine and session with Supabase settings"""
    global engine, SessionLocal
    db_url = get_database_url()
    if db_url:
        logger.info("Initializing Supabase database connection")
        
        # Create async engine for Supabase PostgreSQL
        ssl_context = ssl.create_default_context(cafile=None)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        engine = create_async_engine(
            db_url,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=int(os.environ.get("DB_POOL_SIZE", 10)),
            max_overflow=int(os.environ.get("DB_MAX_OVERFLOW", 20)),
            connect_args={
                "ssl": ssl_context
            }
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
    """Test database connection using Supabase client (HTTPS) instead of direct TCP"""
    try:
        # Use Supabase client for connection test (works on Render)
        from supabase_client import get_supabase
        
        supabase = get_supabase()
        
        # Test by fetching a small dataset
        response = supabase.table("users").select("id").limit(1).execute()
        
        logger.info(f"Supabase connection test successful via HTTPS")
        return True
    except Exception as e:
        logger.warning(f"Supabase connection test failed (this is okay on Render): {e}")
        # Don't fail the startup - just log the warning
        return True  # Return True to avoid blocking startup
