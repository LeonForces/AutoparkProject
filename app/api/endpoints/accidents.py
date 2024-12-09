from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from app.dao.accidents import AccidentDAO
from app.schemas.accidents import SAccident
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.dao.trips import TripsDAO
from app.core.exceptions import AccidentNotFound, TripNotFound

from typing import Annotated
from pydantic import parse_obj_as
from asyncio import sleep


router = APIRouter(prefix="/accident", tags=["Accident"])

@router.post("", description="Добавление аварии")
async def add_accident(trip_id: Annotated[int, Query(description="Id поездки")],
                       degree: Annotated[int, Query(description="Степень повреждения")]):

    trip = await TripsDAO.find_by_id(trip_id)
    if not trip:
        raise TripNotFound

    await AccidentDAO.add(trip_id=trip_id, degree=degree)

@router.get("", description="Получение аварий")
@cache(expire=15)
async def get_accidents():

    await sleep(2)
    accidents = await AccidentDAO.find_all()
    accidents_json = parse_obj_as(list[SAccident], accidents)

    return accidents_json

@router.get("/my_accident", description="Получение всех аварий пользователя")
@cache(expire=15)
async def get_accident(user: Users = Depends(get_current_user)):

    await sleep(2)
    accidents = await AccidentDAO.find_all(user_id=user.id)
    accidents_json = parse_obj_as(list[SAccident], accidents)

    return accidents_json

@router.get("/my_accident/{accident_id}", description="Получение аварии пользователя")
@cache(expire=15)
async def get_accident(accident_id: int):

    await sleep(2)
    accident = await AccidentDAO.find_by_id(accident_id)
    if not accident:
        raise AccidentNotFound
    accident_json = parse_obj_as(SAccident, {
        "id": accident.id,
        "trip_id": accident.trip_id,
        "degree": accident.degree,
    })

    return accident_json

@router.delete("/{accident_id}", description="Удаление аварии")
async def delete_accident(accident_id: int):

    accident = await AccidentDAO.find_by_id(accident_id)
    if not accident:
        raise AccidentNotFound

    await AccidentDAO.delete_(id=accident_id)


@router.put("/{accident_id}", description="Изменение аварии")
async def update_accident(accident_id: int, trip_id: int, degree: str):

    accident = await AccidentDAO.find_by_id(accident_id)
    if not accident:
        raise AccidentNotFound

    trip = TripsDAO.find_by_id(trip_id)
    if not trip:
        raise TripNotFound

    await AccidentDAO.update_(model_id=accident_id, trip_id=trip_id, degree=degree)
