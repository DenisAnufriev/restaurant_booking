from fastapi import FastAPI

from app.routers import tables, reservations

app = FastAPI(title="Restaurant Booking API")

app.include_router(tables.router, prefix="/tables", tags=["Tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
