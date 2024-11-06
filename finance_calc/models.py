from sqlalchemy import Column, Integer, String, Float
from database import Base

class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    amount = Column(Float)
    record_type = Column(String)  # "Доходы" или "Расходы"