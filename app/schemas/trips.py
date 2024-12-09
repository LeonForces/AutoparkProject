from fastapi import Query
from typing import Annotated

from pydantic import BaseModel, field_validator
from datetime import date

import re

#from app.schemas.accidents import SAccident
#from app.schemas.users import SUser
#from app.schemas.drivers import SDriver
#from app.schemas.cars import SCar

from typing import Optional

class STripBase(BaseModel):
    user_id: int
    driver_id: int
    car_id: int
    start_location: str
    end_location: str
    trip_date: date
    cost: float
    rating: int


class STripCreate(STripBase):

    @field_validator('start_location', 'end_location', mode='before')
    def validate_locations(cls, value):
        location_regex = r'^[a-zA-Zа-яА-ЯёЁ0-9\s,\-.]+$'
        if not re.match(location_regex, value):
            raise ValueError("Местоположение должно содержать только буквы, цифры, пробелы, запятые, точки и дефисы.")
        return value.strip()

    @field_validator('cost', mode='before')
    def validate_cost(cls, value):
        cost_regex = r'^\d+\.\d+$'
        if not re.match(cost_regex, str(value)):
            raise ValueError("Стоимость должна быть числом с десятичной точкой.")
        return value

    @field_validator('rating', mode='before')
    def validate_rating(cls, value):
        rating_regex = r'^[1-5]$'
        if not re.match(rating_regex, str(value)):
            raise ValueError("Рейтинг должен быть целым числом от 1 до 5.")
        return value


class STrip(STripBase):
    id: int


    class Config:
        orm_mode = True