from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String

from app.core.db import Base

from datetime import date


class Repairs(Base):
    __tablename__ = "repairs"

    id: Mapped[int] = mapped_column(primary_key=True)

    repair_type: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    date_start: Mapped[date] = mapped_column(nullable=False)
    date_finish: Mapped[date] = mapped_column(nullable=False)

    car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))

    car = relationship("Cars", back_populates="repairs")

    def __str__(self):

        return f"{self.repair_type} | {self.car_id}"
