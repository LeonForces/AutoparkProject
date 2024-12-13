from pydantic import BaseModel, field_validator, EmailStr

from app.schemas.trips import STrip

from typing import Optional, List

import re


class SUserBase(BaseModel):
    login: str
    password: str



class SUserRegister(SUserBase):
    name: str
    email: EmailStr
    telephone: str

    @field_validator('name', mode='before')
    def validate_name(cls, value):
        name_regex = r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$'

        if not re.match(name_regex, value):
            raise ValueError("Имя должно содержать только буквы, пробелы и дефисы.")

        return value.strip()

    @field_validator('telephone', mode='before')
    def validate_telephone(cls, value):
        phone_regex = r'^(\+?\d{1,4}[ \-\.$$]*?)?(\d{3,})?[ \-\.$$]*(\d{3})[ \-\.$$]*(\d{2,})$'

        if not re.match(phone_regex, value):
            raise ValueError("Некорректный формат номера телефона.")

        return value.strip()


class SUserAuth(SUserBase):
    pass


class SUser(SUserBase):
    id: int
    trips: Optional[List[STrip]] = None

    class Config:
        orm_mode = True