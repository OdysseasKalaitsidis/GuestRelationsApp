from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from db import Base  # import Base from db.py



# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    cases = relationship("Case", back_populates="owner")
    followups = relationship("Followup", back_populates="assigned_user")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assigned_user")
    created_tasks = relationship("Task", foreign_keys="Task.assigned_by", back_populates="assigner")
    uploaded_documents = relationship("Document", back_populates="uploader")

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
    
    # New fields - temporarily commented out until migration is run
    # guest = Column(String(255))
    # created = Column(String(100))
    # created_by = Column(String(255))
    # modified = Column(String(100))
    # modified_by = Column(String(255))
    # source = Column(String(255))
    # membership = Column(String(255))
    # case_description = Column(Text)
    # in_out = Column(String(255))

    owner = relationship("User", back_populates="cases")
    followups = relationship("Followup", back_populates="case")




# Followup model
class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    suggestion_text = Column(Text, nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    case = relationship("Case", back_populates="followups")
    assigned_user = relationship("User", back_populates="followups")

# Task model for daily tasks
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=False)  # amenity_list, emails, courtesy_calls
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    due_date = Column(String(50), nullable=False)  # YYYY-MM-DD format
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    created_at = Column(String(50), nullable=False)  # YYYY-MM-DD format
    completed_at = Column(String(50), nullable=True)

    # Relationships
    assigned_user = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    assigner = relationship("User", foreign_keys=[assigned_by], back_populates="created_tasks")

# Document model for RAG system
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, txt
    content = Column(Text, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(String(50), nullable=False)  # YYYY-MM-DD HH:MM:SS format
    file_size = Column(Integer, nullable=True)  # in bytes

    # Relationships
    uploader = relationship("User", back_populates="uploaded_documents")