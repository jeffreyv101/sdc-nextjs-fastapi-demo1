from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database URL - creates a local file database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Blog Post model
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    excerpt = Column(Text)
    content = Column(Text)
    author = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Chat Message model
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()