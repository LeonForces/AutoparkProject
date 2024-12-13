from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from app.dao.trips import TripsDAO
from app.dao.cars import CarsDAO
from app.dao.drivers import DriversDAO
from app.schemas.trips import STrip, STripCreate
from app.models.users import Users
from app.api.dependencies.users.dependencies import get_current_user
from app.core.exceptions import DriverNotFound, TripNotFound, CarNotFound

from typing import Annotated
from pydantic import parse_obj_as
from asyncio import sleep


router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("", description="Добавление поездки")
async def add_trip(trip: STripCreate,
                   user: Users = Depends(get_current_user)):

    driver = await DriversDAO.find_by_id(trip.driver_id)
    if not driver:
        raise DriverNotFound
    car = await CarsDAO.find_by_id(trip.car_id)
    if not car:
        raise CarNotFound

    await TripsDAO.add(user_id=user.id, driver_id=trip.driver_id, car_id=trip.car_id, start_location=trip.start_location,
                       end_location=trip.end_location, trip_date=trip.trip_date, cost=trip.cost, rating=trip.rating)
    return "Success"


@router.get("", description="Получение поездок")
@cache(expire=15)
async def get_trips(user: Users = Depends(get_current_user)):
    await sleep(2)
    trips = await TripsDAO.find_all()
    trips_json = parse_obj_as(list[STrip], trips)
    return trips_json


@router.get("/my_trips", description="Получение всех поездок пользователя")
@cache(expire=15)
async def get_trips(user: Users = Depends(get_current_user)):
    await sleep(2)
    trips = await TripsDAO.find_all(user_id=user.id)
    trips_json = parse_obj_as(list[STrip], trips)
    return  trips_json


@router.delete("/{trip_id}", description="Удаление поездки")
async def delete_trip(trip_id: int,
                      user: Users = Depends(get_current_user)):
    trip = await TripsDAO.find_by_id(trip_id)
    if not trip:
        raise TripNotFound
    await TripsDAO.delete_(id=trip_id)
    return "Success"


@router.put("/{trip_id}", description="Изменение поездки")
async def update_trip(trip_id: int,
                      trip: STripCreate,
                      user: Users = Depends(get_current_user)):

    already_trip = await TripsDAO.find_by_id(trip_id)
    if not already_trip:
        raise TripNotFound
    driver = await DriversDAO.find_by_id(trip.driver_id)
    if not driver:
        raise DriverNotFound
    car = await CarsDAO.find_by_id(trip.car_id)
    if not car:
        raise CarNotFound

    await TripsDAO.update_(model_id=trip_id, user_id=user.id, driver_id=trip.driver_id, car_id=trip.car_id,
                           start_location=trip.start_location, end_location=trip.end_location, trip_date=trip.trip_date,
                           cost=trip.cost, rating=trip.rating)
    return "Success"
