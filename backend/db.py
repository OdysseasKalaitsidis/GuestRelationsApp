import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get MySQL environment variables with defaults
MYSQLUSER = os.getenv('MYSQLUSER')
MYSQLPASSWORD = os.getenv('MYSQLPASSWORD')
MYSQLHOST = os.getenv('MYSQLHOST')
MYSQLPORT = os.getenv('MYSQLPORT', '3306')  # Default to 3306 if not set
MYSQLDATABASE = os.getenv('MYSQLDATABASE')

# Validate required variables
if not all([MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE]):
    raise RuntimeError("Missing required MySQL environment variables: MYSQLUSER, MYSQLPASSWORD, MYSQLHOST, MYSQLDATABASE")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}"
    f"@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
