from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
from models import Base, FinanceRecord
from fastapi.staticfiles import StaticFiles

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель для входных данных
class FinanceRecordInput(BaseModel):
    category: str
    amount: float
    record_type: str

# Путь главной страница
@app.get("/")
async def main():
    return {"Добро пожаловать в финансовый калькулятор"}

# Путь добавления новой записи
@app.post("/add_record/")
async def add_record(record: FinanceRecordInput, db: Session = Depends(get_db)):
    new_record = FinanceRecord(
        category=record.category, amount=record.amount, record_type=record.record_type
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "Запись успешно добавлена"}

# Путь получения всех записей
@app.get("/records/", response_model=List[dict])
async def get_records(db: Session = Depends(get_db)):
    records = db.query(FinanceRecord).all()
    return [{"id": r.id, "category": r.category, "amount": r.amount, "record_type": r.record_type} for r in records]

# Путь вычисления текущего баланса
def calculate_balance(db: Session):
    income = db.query(FinanceRecord).filter(FinanceRecord.record_type == "income").all()
    expense = db.query(FinanceRecord).filter(FinanceRecord.record_type == "expense").all()
    total_income = sum(record.amount for record in income)
    total_expense = sum(record.amount for record in expense)
    return total_income - total_expense

# Путь получения текущего баланса
@app.get("/balance/")
async def get_balance(db: Session = Depends(get_db)):
    balance = calculate_balance(db)
    return {"balance": balance}
