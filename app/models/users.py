from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Users(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    telephone: Mapped[str] = mapped_column(nullable=False)

    trips = relationship("Trips", back_populates="user")

    def __str__(self):

        return f"Пользователь {self.login}"
