from pydantic import BaseModel, field_validator
from datetime import date
import re


class SRepairBase(BaseModel):
    car_id: int
    repair_type: str
    cost: float
    description: str
    date_start: date
    date_finish: date


class SRepairCreate(SRepairBase):

    @field_validator('repair_type', mode='before')
    def validate_repair_type(cls, value):
        type_regex = r'^[a-zA-Z0-9\s\-]+$'
        if not re.match(type_regex, value):
            raise ValueError("Тип ремонта должен содержать только буквы, цифры, пробелы и дефисы.")
        return value.strip()

    @field_validator('description', mode='before')
    def validate_description(cls, value):
        desc_regex = r'^.{10,200}$'
        if not re.match(desc_regex, value):
            raise ValueError("Описание должно содержать от 10 до 200 символов.")
        return value.strip()

    @field_validator('date_start', 'date_finish', mode='before')
    def validate_dates(cls, value):
        try:
            date.fromisoformat(str(value))
        except ValueError as e:
            raise ValueError(f"Дата должна быть в формате ISO (YYYY-MM-DD). Ошибка: {e}")
        return value


class SRepair(SRepairBase):
    id: int


    class Config:
        orm_mode = True
