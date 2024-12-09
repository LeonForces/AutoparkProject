from fastapi import Query
from typing import Annotated

from pydantic import BaseModel, field_validator
import re

#from app.schemas.drivers import SDriver
from app.schemas.repairs import SRepair
from app.schemas.trips import STrip

from typing import Optional, List


class SCarBase(BaseModel):
    driver_id: int
    brand: str
    model: str
    license_plate: str
    reported_issues: int
    vehicle_age: int
    is_working: bool


class SCarCreate(SCarBase):

    @field_validator('brand', 'model', mode='before')
    def validate_brand_model(cls, value):
        brand_model_regex = r'^[a-zA-Z0-9\s\-]+$'
        if not re.match(brand_model_regex, value):
            raise ValueError("Бренд/Модель должны содержать только буквы, цифры, пробелы и дефисы.")
        return value.strip()

    @field_validator('license_plate', mode='before')
    def validate_license_plate(cls, value):
        plate_regex = r'^[a-zA-Z0-9]{6}$'
        if not re.match(plate_regex, value):
            raise ValueError("Номерной знак должен содержать ровно 6 символов (буквы и/или цифры).")
        return value.upper()

    @field_validator('reported_issues', mode='before')
    def validate_reported_issues(cls, value):
        if value < 0:
            raise ValueError("Количество зарегистрированных проблем не может быть отрицательным.")
        return value

    @field_validator('vehicle_age', mode='before')
    def validate_vehicle_age(cls, value):
        if value <= 0:
            raise ValueError("Возраст автомобиля должен быть положительным числом.")
        return value


class SCar(SCarBase):
    id: int

    repairs: Optional[List[SRepair]]
    trips: Optional[List[STrip]]


    class Config:
        orm_mode = True