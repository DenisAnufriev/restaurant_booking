from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.table import Table
from app.schemas.table import TableCreate, TableRead

router = APIRouter()



@router.get("/tables/", response_model=list[TableRead])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()


@router.post("/tables/", response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@router.delete("/tables/{table_id}", status_code=204)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
