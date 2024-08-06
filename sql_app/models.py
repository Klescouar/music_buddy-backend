from sqlalchemy import Column, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    spotify_id = Column(String, index=True)

    history = relationship("History", back_populates="owner")


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    search = Column(String, index=True)
    suggestions = Column(ARRAY(String), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="history")
