import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

raw_mysql_url = os.getenv("MYSQL_URL")
database_url = raw_mysql_url.replace("mysql://", "mysql+pymysql://") if raw_mysql_url else os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("No database URL found. Set MYSQL_URL or DATABASE_URL.")

print("Using DATABASE_URL:", database_url)  # debug log

engine = create_engine(database_url, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
