from fastapi import APIRouter, Depends, Query

from fastapi_cache.decorator import cache

from typing import Annotated

from pydantic import parse_obj_as

from app.schemas.cars import SCar, SCarCreate
from app.dao.cars import CarsDAO
from app.dao.drivers import DriversDAO
from app.core.exceptions import CarAlreadyExists, CarNotFound, DriverNotFound
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user


router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("", description="Добавление автомобиля")
async def add_car(car: SCarCreate,
                  user: Users = Depends(get_current_user)):

    already_car = await CarsDAO.find_by_number(license_plate=car.license_plate)
    if already_car:
        raise CarAlreadyExists
    driver = await DriversDAO.find_by_id(car.driver_id)
    if not driver:
        raise DriverNotFound

    await CarsDAO.add(driver_id=car.driver_id, brand=car.brand, model=car.model, license_plate=car.license_plate.upper(),
                      reported_issues=car.reported_issues, vehicle_age=car.vehicle_age, is_working=car.is_working)
    return "Success"


@router.get("", description="Получение всех автомобилей")
@cache(expire=15)
async def get_cars(user: Users = Depends(get_current_user)):
    cars = await CarsDAO.find_all()
    cars_json = parse_obj_as(list[SCar], cars)
    return cars_json


@router.delete("/{car_id}", description="Удаление автомобиля")
async def delete_car(car_id: int,
                     user: Users = Depends(get_current_user)):

    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound

    await CarsDAO.delete_(id=car_id)
    return "Success"


@router.put("/{car_id}", description="Изменение автомобиля")
async def update_car(car_id: int,
                     car: SCarCreate,
                     user: Users = Depends(get_current_user)):

    already_car = await CarsDAO.find_by_id(car_id)
    if not already_car:
        raise CarNotFound

    already_car = await CarsDAO.find_by_number(license_plate=car.license_plate)
    if not already_car:
        raise CarAlreadyExists

    driver = await DriversDAO.find_by_id(car.driver_id)
    if not driver:
        raise DriverNotFound

    await CarsDAO.update_(model_id=car_id, driver_id=car.driver_id, brand=car.brand, model=car.model,
                          license_plate=car.license_plate.upper(), reported_issues=car.reported_issues,
                          vehicle_age=car.vehicle_age, is_working=car.is_working)
    return "Success"
