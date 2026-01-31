from typing import Annotated, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Booking
from database import SessionLocal
from datetime import datetime, date, time

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class BookingRequest(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    phone: str = Field(min_length=7)
    service: str = Field(min_length=3)
    notes: Optional[str] = ""
    time: time
    date: date
    status: Optional[str] = ""
    scheduled_at: Optional[datetime] = None


class BookingResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    service: str
    notes: str | None
    time: time
    date: date
    status: Optional[str] = 'pending'
    scheduled_at: datetime


@router.get('/bookings', status_code=status.HTTP_200_OK)
async def get_bookings(db: db_dependency):
    return db.query(Booking).all()


@router.get('/booking/{id}', status_code=status.HTTP_200_OK)
async def get_booking(db: db_dependency, id: int = Path(gt=0)):
    booking_model = db.query(Booking).filter(Booking.id == id).first()

    if booking_model is not None:
        return booking_model
    raise HTTPException(status_code=404, detail='Booking not found')


def build_scheduled_at(
        d: date,
        t: time,
        tz_name: str = "America/New_York"
) -> datetime:
    local_dt = datetime.combine(d, t).replace(
        tzinfo=ZoneInfo(tz_name)
    )
    return local_dt.astimezone(ZoneInfo("UTC"))


@router.post('/booking', status_code=status.HTTP_201_CREATED, response_model=BookingResponse)
async def create_booking(db: db_dependency, booking_request: BookingRequest):
    print("INCOMING date:", booking_request.date)
    print("INCOMING time:", booking_request.time)

    scheduled_at_utc = build_scheduled_at(booking_request.date, booking_request.time)

    booking = Booking(
        name=booking_request.name,
        email=booking_request.email,
        phone=booking_request.phone,
        service=booking_request.service,
        notes=booking_request.notes,
        date=booking_request.date,
        time=booking_request.time,
        scheduled_at=scheduled_at_utc,
        status=booking_request.status
    )

    double_booked = select(Booking.id).where(
        and_(
            Booking.date == booking_request.date,
            Booking.time == booking_request.time,
            Booking.scheduled_at == scheduled_at_utc
        )).limit(1)

    double_booked_conflict = db.execute(double_booked).scalar_one_or_none()
    if double_booked_conflict:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='This time slot is book. pleease choose different time slot or date')

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.put('/booking/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_booking(db: db_dependency, booking_request: BookingRequest, booking_id: int = Path(gt=0)):
    booking_model = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_model is None:
        raise HTTPException(status_code=404, detail='Booking not found')

    booking_model.name = booking_request.name
    booking_model.email = booking_request.email
    booking_model.phone = booking_request.phone
    booking_model.service = booking_request.service
    booking_model.notes = booking_request.notes
    booking_model.time = booking_request.time
    booking_model.status = booking_request.status
    booking_request.scheduled_at = booking_request.scheduled_at

    db.add(booking_model)
    db.commit()


@router.delete('/booking/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(db: db_dependency, booking_id: int = Path(gt=0)):
    booking_model = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking_model is None:
        raise HTTPException(status_code=404, detail='Booking not found')
    db.query(Booking).filter(Booking.id == booking_id).delete()

    db.commit()
