from fastapi import Query
from typing import Annotated

from pydantic import BaseModel, field_validator
import re

from app.schemas.repairs import SRepair
from app.schemas.trips import STrip


from typing import Optional, List


class SCarBase(BaseModel):
    driver_id: Annotated[int, Query(description="Id водителя")]
    brand: Annotated[str, Query(description="Бренд")]
    model: Annotated[str, Query(description="Модель")]
    license_plate: Annotated[str, Query(description="Номерной знак")]
    reported_issues: Annotated[int, Query(description="Зарегистрированные проблемы")]
    vehicle_age: Annotated[int, Query(description="Возраст транспортного средства")]
    is_working: Annotated[bool, Query(description="В рабочем состоянии")]



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
        if value < 0:
            raise ValueError("Возраст автомобиля должен быть положительным числом.")
        return value


class SCar(SCarBase):
    id: int

    repairs: Optional[List[SRepair]] = None
    trips: Optional[List[STrip]] = None



    class Config:
        orm_mode = True