from sqlalchemy import Column, Integer,String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from .database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True, nullable=False )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    relesed = Column(Boolean, nullable=False, server_default=text('true'))
    modified = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
