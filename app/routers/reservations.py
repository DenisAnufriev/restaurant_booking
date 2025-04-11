from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationRead as ReservationSchema
from app.services.reservation_logic import is_slot_available

router = APIRouter()


@router.post("/reservations/", response_model=ReservationSchema)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Проверка доступности времени для бронирования
    if not is_slot_available(db, reservation.table_id, reservation.reservation_time, reservation.duration_minutes):
        raise HTTPException(status_code=400, detail="The time slot is already taken")

    # Создание нового бронирования, если слот доступен
    db_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes,
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation
