from db import Base, engine
from models import User, Case, Followup

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
