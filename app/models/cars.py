from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String

from app.core.db import Base


class Cars(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    lisense_plate: Mapped[str] = mapped_column(nullable=False)
    reported_issues: Mapped[int] = mapped_column(nullable=False)
    vehicle_age: Mapped[int] = mapped_column(nullable=False)
    is_working: Mapped[bool] = mapped_column(nullable=False)

    driver_id: Mapped[int] = mapped_column(ForeignKey('drivers.id'))

    driver = relationship("Drivers", back_populates="cars")
    repairs = relationship("Repairs", back_populates="car")
    trips = relationship("Trips", back_populates="car")

    def __str__(self):

        return f"{self.bramd} | {self.model}"
