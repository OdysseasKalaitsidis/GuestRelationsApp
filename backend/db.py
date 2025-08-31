from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Prefer MYSQL_URL (Railway), fallback to DATABASE_URL (local)
raw_mysql_url = os.getenv("MYSQL_URL")
database_url = None

if raw_mysql_url:
    database_url = raw_mysql_url.replace("mysql://", "mysql+pymysql://")
else:
    database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("No database URL found. Set MYSQL_URL or DATABASE_URL in your environment.")

print("Using DATABASE_URL:", database_url)

engine = create_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
