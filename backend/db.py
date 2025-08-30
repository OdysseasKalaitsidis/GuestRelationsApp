from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

load_dotenv()

# Use Railway's DATABASE_URL environment variable if available, otherwise fall back to local config
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL is:", DATABASE_URL)  # Debug logging

if not DATABASE_URL:
    # Fallback to local development configuration
    db_password = os.getenv("DB_PASSWORD", "")
    encoded_password = quote_plus(db_password)
    DATABASE_URL = f"mysql+pymysql://myuser:{encoded_password}@localhost:3306/mydb"
    print("Using fallback DATABASE_URL:", DATABASE_URL)  # Debug logging

engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Disable SQL logging for better performance
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections every hour
    pool_size=10,  # Connection pool size
    max_overflow=20  # Maximum overflow connections
)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Prevent expired object issues
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
