from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    topic = Column(String(255))
    target_audience = Column(String(100))
    audience_type = Column(String(50), default="general")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="projects")
    lessons = relationship("Lesson", back_populates="project", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="project", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0)
    learning_objectives = Column(JSON, default=list)
    content_standard = Column(JSON, default=dict)
    content_simplified = Column(JSON, default=dict)
    content_accessibility = Column(JSON, default=dict)
    duration_minutes = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="lessons")
    units = relationship("Unit", back_populates="lesson", cascade="all, delete-orphan")

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(JSON, default=dict)
    order_index = Column(Integer, default=0)
    activities = Column(JSON, default=list)
    assessments = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    lesson = relationship("Lesson", back_populates="units")

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    interactivity_score = Column(Float, default=0)
    multimedia_score = Column(Float, default=0)
    assessment_score = Column(Float, default=0)
    inclusiveness_score = Column(Float, default=0)
    overall_score = Column(Float, default=0)
    feedback = Column(Text)
    suggestions = Column(JSON, default=list)
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="evaluations")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), default="warning")
    message = Column(Text, nullable=False)
    suggestion = Column(Text)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
