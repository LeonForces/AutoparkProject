from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

from datetime import date


class Drivers(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    telephone: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    driving_experience: Mapped[int] = mapped_column(nullable=False)
    date_of_joining: Mapped[date] = mapped_column(nullable=False)

    cars = relationship("Cars", back_populates="driver")
    trips = relationship("Trips", back_populates="driver")

    def __str__(self):

        return f"{self.name} | {self.telephone}"
