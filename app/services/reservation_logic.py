from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models.reservation import Reservation


def is_slot_available(
        db: Session, table_id: int, reservation_time: datetime, duration_minutes: int
) -> bool:
    """Проверка, доступен ли слот для бронирования"""
    end_time = reservation_time + timedelta(minutes=duration_minutes)

    overlapping_reservation = (
        db.query(Reservation)
        .filter(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            Reservation.reservation_time + timedelta(minutes=duration_minutes) > reservation_time,
        )
        .first()
    )
    return overlapping_reservation is None
