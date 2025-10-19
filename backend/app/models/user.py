from sqlalchemy import Column, Integer, String,Date,Boolean
from app.config.database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String, unique=True, index=True,nullable=False)
    mobile= Column(String, unique=True, index=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    dob = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    agreed = Column(Boolean, nullable=False)
    portfolios = relationship("Portfolio", back_populates="user")
