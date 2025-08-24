from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from db import Base  # import Base from db.py

# Enum for Followup status
class FollowupStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    cases = relationship("Case", back_populates="owner")
    followups = relationship("Followup", back_populates="assigned_user")

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    room = Column(String(50))
    status = Column(String(50))
    importance = Column(String(50))
    type = Column(String(50))
    title = Column(Text)  # rename "case" -> "title"
    action = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Made nullable

    owner = relationship("User", back_populates="cases")
    followups = relationship("Followup", back_populates="case")




# Followup model
class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    suggestion_text = Column(Text, nullable=False)
    status = Column(Enum(FollowupStatus, native_enum=False), default=FollowupStatus.pending)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    case = relationship("Case", back_populates="followups")
    assigned_user = relationship("User", back_populates="followups")
