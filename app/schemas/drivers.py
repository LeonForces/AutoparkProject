from fastapi import Query
from typing import Annotated

from pydantic import BaseModel, field_validator
from datetime import date
import re

from app.schemas.cars import SCar
from app.schemas.trips import STrip

from typing import Optional, List


class SDriverBase(BaseModel):
    name: str
    gender: str
    telephone: str
    rating: float
    driving_experience: int
    date_of_joining: date


class SDriverCreate(SDriverBase):

    @field_validator('name', mode='before')
    def validate_name(cls, value):
        name_regex = r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$'
        if not re.match(name_regex, value):
            raise ValueError("Имя должно содержать только буквы, пробелы и дефисы.")
        return value.strip()

    @field_validator('gender', mode='before')
    def validate_gender(cls, value):
        gender_regex = r'^(male|female)$'
        if not re.match(gender_regex, value.lower()):
            raise ValueError("Пол должен быть указан как 'male' или 'female'.")
        return value.lower()

    @field_validator('telephone', mode='before')
    def validate_telephone(cls, value):
        phone_regex = r'^(\+?\d{1,4}[ \-\.$$]*?)?(\d{3,})?[ \-\.$$]*(\d{3})[ \-\.$$]*(\d{2,})$'
        if not re.match(phone_regex, value):
            raise ValueError("Некорректный формат номера телефона.")
        return value.strip()

    @field_validator('rating', mode='before')
    def validate_rating(cls, value):
        rating_regex = r'^\d+\.\d+$'
        if not re.match(rating_regex, str(value)):
            raise ValueError("Рейтинг должен быть числом с десятичной точкой.")
        return value

    @field_validator('date_of_joining', mode='before')
    def validate_date_of_joining(cls, value):
        try:
            date.fromisoformat(str(value))
        except ValueError as e:
            raise ValueError(f"Дата присоединения должна быть в формате ISO (YYYY-MM-DD). Ошибка: {e}")
        return value


class SDriver(SDriverBase):
    id: int
    cars: Optional[List[SCar]]
    trips: Optional[List[STrip]]

    class Config:
        orm_mode = True