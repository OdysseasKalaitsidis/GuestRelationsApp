import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

raw_mysql_url = os.getenv("MYSQL_URL")
if not raw_mysql_url:
    raise RuntimeError("No MYSQL_URL set in environment!")

# Convert to SQLAlchemy format
database_url = raw_mysql_url.replace("mysql://", "mysql+pymysql://")

engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
