from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime,JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    portfolio_name = Column(String, nullable=False)
    tenure = Column(Integer, nullable=False)  
    amount = Column(Numeric, nullable=False)
    risk_profile = Column(String, nullable=False) 
    recommendation = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="portfolios")
