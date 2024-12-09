from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String

from app.core.db import Base


class Accidents(Base):
    __tablename__ = "accidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    degree: Mapped[str] = mapped_column(nullable=False)

    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id'))

    trip = relationship("Trips", back_populates="accidents")

    def __str__(self):

        return f"{self.trip_id} | {self.degree}"
