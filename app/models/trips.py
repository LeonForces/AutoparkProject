from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.core.db import Base

from datetime import date


class Trips(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)

    start_location: Mapped[str] = mapped_column(nullable=False)
    end_location: Mapped[str] = mapped_column(nullable=False)
    trip_date: Mapped[date] = mapped_column(nullable=False)
    cost: Mapped[float] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    driver_id: Mapped[int] = mapped_column(ForeignKey('drivers.id'))
    car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))

    user = relationship("Users", back_populates="trips")
    driver = relationship("Drivers", back_populates="trips")
    car = relationship("Cars", back_populates="trips")
    accidents = relationship("Accidents", back_populates="trip")

    def __str__(self):

        return f"{self.start_location} | {self.end_location} | {self.trip_date}"
