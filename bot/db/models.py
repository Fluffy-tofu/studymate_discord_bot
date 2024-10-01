from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    _is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    discord_id = Column(String(20), unique=True, nullable=True)
    discord_avatar = Column(String(100), nullable=True)
    discord_global_name = Column(String(100), nullable=True)

    study_sessions = relationship("StudySession", back_populates="user", foreign_keys="StudySession.discord_user_id")
    todos = relationship("Todo", back_populates="user")


class StudySession(Base):
    __tablename__ = 'study_sessions'
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String(20), ForeignKey('users.discord_id'), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Float)  # In hours
    subject = Column(String(50), nullable=False)

    user = relationship("User", back_populates="study_sessions", foreign_keys=[discord_user_id])


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(String(20), ForeignKey('users.discord_id'), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(TIMESTAMP)
    status = Column(String(20))
    created_at = Column(DateTime)

    user = relationship("User", back_populates="todos", foreign_keys=[discord_user_id])
