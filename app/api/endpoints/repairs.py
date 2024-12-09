from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from app.dao.cars import CarsDAO
from app.dao.repairs import RepairsDAO
from app.schemas.repairs import SRepair
from app.models.repairs import Repairs
from app.api.dependencies.users.dependencies import get_current_user
from app.dao.trips import TripsDAO
from app.core.exceptions import RepairNotFound, TripNotFound, CarNotFound

from typing import Annotated
from pydantic import parse_obj_as
from asyncio import sleep
from datetime import date

router = APIRouter(prefix="/repairs", tags=["Repairs"])

@router.post("", description="Добавление ремонта")
async def add_repair(repair_type: Annotated[str, Query(description="Тип ремонта")],
                     car_id: Annotated[int, Query(description="Id автомобиля")],
                     cost: Annotated[float, Query(description="Стоимость")],
                     description: Annotated[str, Query(description="Описание")],
                     date_start: Annotated[date, Query(description="Дата начала ремонта")],
                     date_finish: Annotated[date, Query(description="Дата завершения ремонта")]):

    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound

    await RepairsDAO.add(repair_type=repair_type, car_id=car_id, cost=cost, description=description,
                         date_start=date_start, date_finish=date_finish)


@router.get("", description="Получение ремонтов")
@cache(expire=15)
async def get_repairs():

    await sleep(2)
    repairs = await RepairsDAO.find_all()
    repairs_json = parse_obj_as(list[SRepair], repairs)

    return repairs_json


@router.get("/{car_id}", description="Получение всех ремонтов автомобиля")
@cache(expire=15)
async def get_repairs(car_id: int):

    await sleep(2)
    car = CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    filter = Repairs.car_id == car_id
    repairs = RepairsDAO.find_with_filters(filter)
    repairs_json = parse_obj_as(list[SRepair], repairs)

    return  repairs_json


@router.delete("/{repair_id}", description="Удаление ремонта")
async def delete_repair(repair_id: int):

    repair = await RepairsDAO.find_by_id(repair_id)
    if not repair:
        raise RepairNotFound

    await RepairsDAO.delete_(id=repair_id)


@router.put("/{repair_id}", description="Изменение ремонта")
async def update_rapair(repair_id: int,
                        repair_type: Annotated[str, Query(description="Тип ремонта")],
                        car_id: Annotated[int, Query(description="Id автомобиля")],
                        cost: Annotated[float, Query(description="Стоимость")],
                        description: Annotated[str, Query(description="Описание")],
                        date_start: Annotated[date, Query(description="Дата начала ремонта")],
                        date_finish: Annotated[date, Query(description="Дата завершения ремонта")]):

    repair = await RepairsDAO.find_by_id(repair_id)
    if not repair:
        raise RepairNotFound
    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound

    await RepairsDAO.update_(model_id=repair_id, repair_type=repair_type, car_id=car_id, cost=cost,
                             description=description, date_start=date_start, date_finish=date_finish)
