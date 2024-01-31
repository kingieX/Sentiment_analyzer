from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime,Float
from sqlalchemy.orm import relationship
from datetime import datetime
import database


class User(database.Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(DateTime, nullable=False, default=datetime.utcnow)

    # One-to-One relationship with PreferenceSetting
    preference_setting = relationship("PreferenceSetting", uselist=False, back_populates="user")

    # One-to-Many relationship with SentimentResult
    sentiment_results = relationship("SentimentResult", back_populates="user")

    # One-to-Many relationship with TextInput
    text_inputs = relationship("TextInput", back_populates="user")


class Token(database.Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450),primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.utcnow)

class TextInput(database.Base):

    __tablename__ = "textinputs"

    id = Column(Integer, primary_key=True)
    text_content = Column(String)
    text_title = Column(String)
    language = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Many-to-One relationship with User
    user = relationship("User", back_populates="text_inputs")

class SentimentResult(database.Base):

    __tablename__ = "sentiment_results"

    id = Column(Integer, primary_key=True, index=True)
    text_id = Column(Integer, ForeignKey("textinputs.id"))
    score = Column(Float)
    label = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Many-to-One relationship with User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sentiment_results")

class PreferenceSetting(database.Base):

    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    theme = Column(String)
    notification = Column(Boolean)
    language_preference = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # One-to-One relationship with User
    user = relationship("User", back_populates="preference_setting")