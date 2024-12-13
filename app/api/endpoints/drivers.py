from fastapi import APIRouter, Depends, Body
from fastapi_cache.decorator import cache

from app.dao.drivers import DriversDAO
from app.schemas.drivers import SDriver, SDriverCreate
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.core.exceptions import DriverNotFound

from pydantic import parse_obj_as
from asyncio import sleep

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("", description="Добавление водителя")
async def add_driver(driver: SDriverCreate = Body (...),
                     user: Users = Depends(get_current_user)):

    await DriversDAO.add(name=driver.name, gender=driver.gender, telephone=driver.telephone, rating=driver.rating,
                         driving_experience=driver.driving_experience, date_of_joining=driver.date_of_joining)
    return "Success"

@router.get("", description="Получение водителей")
@cache(expire=15)
async def get_drivers(user: Users = Depends(get_current_user)):
    await sleep(2)

    drivers = await DriversDAO.find_all()
    drivers_json = parse_obj_as(list[SDriver], drivers)

    return drivers_json


@router.delete("/{driver_id}", description="Удаление водителя")
async def delete_driver(driver_id: int,
                        user: Users = Depends(get_current_user)):
    driver = await DriversDAO.find_by_id(driver_id)
    if not driver:
        raise DriverNotFound
    await DriversDAO.delete_(id=driver_id)
    return "Success"


@router.put("/{driver_id}", description="Изменение водителя")
async def update_driver(driver_id: int,
                        driver: SDriverCreate,
                        user: Users = Depends(get_current_user)):
    already_driver = await DriversDAO.find_by_id(driver_id)
    if not already_driver:
        raise DriverNotFound

    await DriversDAO.update_(model_id=driver_id, name=driver.name, gender=driver.gender, telephone=driver.telephone,
                             rating=driver.rating, driving_experience=driver.driving_experience,
                             date_of_joining=driver.date_of_joining)
    return "Success"
