from pydantic import BaseModel, field_validator
import re


class SAccidentBase(BaseModel):
    trip_id: int
    degree: str


class SAccidentCreate(SAccidentBase):

    @field_validator('degree', mode='before')
    def validate_degree(cls, value):
        degree_regex = r'^(minor|moderate|severe)$'
        if not re.match(degree_regex, value.lower()):
            raise ValueError("Степень ДТП должна быть указана как 'minor', 'moderate' или 'severe'.")
        return value.lower()


class SAccident(SAccidentBase):
    id: int


    class Config:
        orm_mode = True