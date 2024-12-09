from app.dao.base import BaseDAO
from app.models.trips import Trips


class TripsDAO(BaseDAO):

    model = Trips
