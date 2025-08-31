from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

load_dotenv()

raw_mysql_url = os.getenv("MYSQL_URL")

if raw_mysql_url:
    DATABASE_URL = raw_mysql_url.replace("mysql://", "mysql+pymysql://")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")  # fallback if you define it manually

print("DATABASE_URL is:", DATABASE_URL)  # Debug

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
