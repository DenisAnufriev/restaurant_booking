from fastapi import FastAPI
import uvicorn
from app.routers import tables, reservations

app = FastAPI(title="Restaurant Booking API")

app.include_router(tables.router, prefix="/tables", tags=["Tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=8000)