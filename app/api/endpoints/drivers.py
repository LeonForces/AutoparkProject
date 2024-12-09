from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from app.dao.drivers import DriversDAO
from app.schemas.drivers import SDriver
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.dao.trips import TripsDAO
from app.core.exceptions import DriverNotFound

from typing import Annotated
from pydantic import parse_obj_as
from asyncio import sleep
from datetime import date

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("", description="Добавление водителя")
async def add_driver(name: Annotated[str, Query(description="Имя водителя")],
                     gender: Annotated[str, Query(description="Пол")],
                     telephone: Annotated[str, Query(description="Номер телефона")],
                     rating: Annotated[float, Query(description="Рейтинг")],
                     driving_experience: Annotated[int, Query(description="Опыт вождения")],
                     date_of_joining: Annotated[date, Query(description="Дата вступления")]):

    await DriversDAO.add(name=name, gender=gender, telephone=telephone, rating=rating,
                         driving_experience=driving_experience, date_of_joining=date_of_joining)

@router.get("", description="Получение водителей")
@cache(expire=15)
async def get_drivers():
    await sleep(2)
    drivers = await DriversDAO.find_all()
    drivers_json = parse_obj_as(list[SDriver], drivers)
    return drivers_json


@router.delete("/{driver_id}", description="Удаление водителя")
async def delete_driver(driver_id: int):
    driver = await DriversDAO.find_by_id(driver_id)
    if not driver:
        raise DriverNotFound
    await DriversDAO.delete_(id=driver_id)


@router.put("/{driver_id}", description="Изменение водителя")
async def update_driver(driver_id: int,
                        name: Annotated[str, Query(description="Имя водителя")],
                        gender: Annotated[str, Query(description="Пол")],
                        telephone: Annotated[str, Query(description="Номер телефона")],
                        rating: Annotated[float, Query(description="Рейтинг")],
                        driving_experience: Annotated[int, Query(description="Опыт вождения")],
                        date_of_joining: Annotated[date, Query(description="Дата вступления")]):
    driver = await DriversDAO.find_by_id(driver_id)
    if not driver:
        raise DriverNotFound

    await DriversDAO.update_(model_id=driver_id, name=name, gender=gender, telephone=telephone, rating=rating,
                         driving_experience=driving_experience, date_of_joining=date_of_joining)
