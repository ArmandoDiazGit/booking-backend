from datetime import timezone, datetime

from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Date, Time


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    service = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    time = Column(Time, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
