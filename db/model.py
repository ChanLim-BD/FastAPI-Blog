from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)

    # User와 Blog 간의 관계 정의
    blogs = relationship("Blog", back_populates="author")


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=False)
    image_loc = Column(String(300), nullable=True)
    modified_dt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Blog와 User 간의 관계 정의
    author = relationship("User", back_populates="blogs")
