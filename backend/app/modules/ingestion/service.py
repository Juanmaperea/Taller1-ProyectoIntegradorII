#modules/ingestion/service.py
from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.utils.excel_parser import parse_excel
from datetime import datetime

def process_excel(file, db: Session, user_id: int):

    df = parse_excel(file)

    records_inserted = 0

    for _, row in df.iterrows():
        expense = Expense(
            description=row["description"],
            category=row.get("category"),
            amount=float(row["amount"]),
            date=row["date"] if isinstance(row["date"], datetime)
            else datetime.strptime(str(row["date"]), "%Y-%m-%d"),
            user_id=user_id
        )

        db.add(expense)
        records_inserted += 1

    db.commit()

    return records_inserted