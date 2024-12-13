from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.dao.cars import CarsDAO
from app.dao.repairs import RepairsDAO
from app.schemas.repairs import SRepair, SRepairCreate
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.core.exceptions import RepairNotFound, CarNotFound

from pydantic import parse_obj_as
from asyncio import sleep

router = APIRouter(prefix="/repairs", tags=["Repairs"])

@router.post("", description="Добавление ремонта")
async def add_repair(repair : SRepairCreate,
                     user: Users = Depends(get_current_user)):

    car = await CarsDAO.find_by_id(repair.car_id)
    if not car:
        raise CarNotFound

    await RepairsDAO.add(repair_type=repair.repair_type, car_id=repair.car_id, cost=repair.cost, description=repair.description,
                         date_start=repair.date_start, date_finish=repair.date_finish)
    return "Success"


@router.get("", description="Получение ремонтов")
@cache(expire=15)
async def get_repairs(user: Users = Depends(get_current_user)):

    await sleep(2)
    repairs = await RepairsDAO.find_all()
    repairs_json = parse_obj_as(list[SRepair], repairs)

    return repairs_json


@router.get("/{car_id}", description="Получение всех ремонтов автомобиля")
@cache(expire=15)
async def get_repairs(car_id: int,
                      user: Users = Depends(get_current_user)):

    await sleep(2)
    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound

    repairs = await RepairsDAO.find_all(car_id=car_id)
    repairs_json = parse_obj_as(list[SRepair], repairs)

    return  repairs_json


@router.delete("/{repair_id}", description="Удаление ремонта")
async def delete_repair(repair_id: int,
                        user: Users = Depends(get_current_user)):

    repair = await RepairsDAO.find_by_id(repair_id)
    if not repair:
        raise RepairNotFound

    await RepairsDAO.delete_(id=repair_id)
    return "Success"


@router.put("/{repair_id}", description="Изменение ремонта")
async def update_repair(repair_id: int,
                        repair: SRepairCreate,
                        user: Users = Depends(get_current_user)):

    already_repair = await RepairsDAO.find_by_id(repair_id)
    if not already_repair:
        raise RepairNotFound
    car = await CarsDAO.find_by_id(repair.car_id)
    if not car:
        raise CarNotFound

    await RepairsDAO.update_(model_id=repair_id, repair_type=repair.repair_type, car_id=repair.car_id, cost=repair.cost,
                             description=repair.description, date_start=repair.date_start, date_finish=repair.date_finish)
    return "Success"
