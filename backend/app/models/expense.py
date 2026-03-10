from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String)
    amount = Column(Float)
    date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="expenses")