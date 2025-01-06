from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    read_rules = Column(Boolean, default=False)
    themes = relationship("Theme", back_populates="user")


class Theme(Base):
    __tablename__ = "themes"
    theme_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    suggestion_time = Column(DateTime, default=datetime.utcnow)
    theme = Column(String, nullable=False)
    user = relationship("User", back_populates="themes")
