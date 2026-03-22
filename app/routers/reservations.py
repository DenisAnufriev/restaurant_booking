from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.reservation import Reservation
from app.schemas.reservation import (
    ReservationCreate,
    ReservationRead,
)
from app.services.reservation_logic import is_slot_available

router = APIRouter()


@router.get("/", response_model=list[ReservationRead])
def get_all_reservations(db: Session = Depends(get_db)):
    """Получить все бронирования"""
    reservations = db.query(Reservation).options(joinedload(Reservation.table)).all()
    return [
        ReservationRead(
            id=r.id,
            customer_name=r.customer_name,
            table_id=r.table_id,
            reservation_time=r.reservation_time,
            duration_minutes=r.duration_minutes,
            table_location=r.table.location,
        )
        for r in reservations
    ]


@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    Создаёт новое бронирование столика, проверяя доступность времени и возвращая полную информацию о бронировании.
    """
    if not is_slot_available(
            db,
            reservation.table_id,
            reservation.reservation_time,
            reservation.duration_minutes,
    ):
        raise HTTPException(
            status_code=400,
            detail="На это время столик уже забронирован. Выберите другое время."
        )

    db_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes,
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    db.refresh(db_reservation, attribute_names=["table"])

    return ReservationRead(
        id=db_reservation.id,
        customer_name=db_reservation.customer_name,
        table_id=db_reservation.table_id,
        reservation_time=db_reservation.reservation_time,
        duration_minutes=db_reservation.duration_minutes,
        table_location=db_reservation.table.location,  # Добавляем location
    )


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """Удалить бронь по ID"""
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Резервация не найдена")

    db.delete(reservation)
    db.commit()
    return {"message": "Резервация столика удалена"}
