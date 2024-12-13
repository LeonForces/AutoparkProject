from fastapi import Query
from typing import List

from pydantic import BaseModel, field_validator
from datetime import date

import re

from typing import Optional

from app.schemas.accidents import SAccident


class STripBase(BaseModel):
    driver_id: int
    car_id: int
    start_location: str
    end_location: str
    trip_date: date
    cost: float
    rating: int


class STripCreate(STripBase):

    @field_validator('trip_date', mode='before')
    def validate_dates(cls, value):
        try:
            date.fromisoformat(str(value))
        except ValueError as e:
            raise ValueError(f"Дата должна быть в формате ISO (YYYY-MM-DD). Ошибка: {e}")
        return value

    @field_validator('start_location', 'end_location', mode='before')
    def validate_locations(cls, value):
        location_regex = r'^[a-zA-Zа-яА-ЯёЁ0-9\s,\-.]+$'
        if not re.match(location_regex, value):
            raise ValueError("Местоположение должно содержать только буквы, цифры, пробелы, запятые, точки и дефисы.")
        return value.strip()

    @field_validator('rating', mode='before')
    def validate_rating(cls, value):
        if value < 0 or value > 10:
            raise ValueError("Рейтинг должен быть целым числом от 0 до 10.")
        return value


class STrip(STripBase):
    id: int
    user_id: int
    accidents: Optional[List[SAccident]] = None


    class Config:
        orm_mode = True