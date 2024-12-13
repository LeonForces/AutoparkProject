from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.dao.accidents import AccidentDAO
from app.schemas.accidents import SAccident, SAccidentCreate
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.dao.trips import TripsDAO
from app.core.exceptions import AccidentNotFound, TripNotFound

from pydantic import parse_obj_as
from asyncio import sleep


router = APIRouter(prefix="/accidents", tags=["Accidents"])

@router.post("", description="Добавление аварии")
async def add_accident(accident: SAccidentCreate,
                       user: Users = Depends(get_current_user)):

    trip = await TripsDAO.find_by_id(accident.trip_id)
    if not trip:
        raise TripNotFound

    await AccidentDAO.add(trip_id=accident.trip_id, degree=accident.degree)
    return "Success"

@router.get("", description="Получение всех аварий")
@cache(expire=15)
async def get_accidents(user: Users = Depends(get_current_user)):

    await sleep(2)
    accidents = await AccidentDAO.find_all()
    accidents_json = parse_obj_as(list[SAccident], accidents)

    return accidents_json

@router.delete("/{accident_id}", description="Удаление аварии")
async def delete_accident(accident_id: int, user: Users = Depends(get_current_user)):

    accident = await AccidentDAO.find_by_id(accident_id)
    if not accident:
        raise AccidentNotFound

    await AccidentDAO.delete_(id=accident_id)
    return "Success"


@router.put("/{accident_id}", description="Изменение аварии")
async def update_accident(accident_id: int,
                          accident: SAccidentCreate,
                          user: Users = Depends(get_current_user)):

    already_accident = await AccidentDAO.find_by_id(accident_id)
    if not already_accident:
        raise AccidentNotFound

    trip = TripsDAO.find_by_id(accident.trip_id)
    if not trip:
        raise TripNotFound

    await AccidentDAO.update_(model_id=accident_id, trip_id=accident.trip_id, degree=accident.degree)
    return "Success"
