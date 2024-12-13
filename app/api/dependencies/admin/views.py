from sqladmin import ModelView

from app.models.cars import Cars
from app.models.users import Users

from app.models.accidents import Accidents
from app.models.drivers import Drivers
from app.models.repairs import Repairs
from app.models.trips import Trips


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.login, Users.name, Users.email, Users.telephone]
    column_details_exclude_list = [Users.hashed_password]

    can_edit = False
    can_create = True
    can_delete = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class CarAdmin(ModelView, model=Cars):
    column_list = [Cars.id, Cars.brand, Cars.model, Cars.license_plate, Cars.reported_issues, Cars.vehicle_age,
                   Cars.is_working]
    can_delete = True
    can_create = False
    can_edit = False

    name = "Car"
    name_plural = "Cars"
    icon = "fa-solid fa-car"


class AccidentAdmin(ModelView, model=Accidents):
    column_list = []
    can_delete = True
    can_create = False
    can_edit = False

    name = "Accident"
    name_plural = "Accidents"
    icon = "fa-solid fa-accident"


class DriverAdmin(ModelView, model=Drivers):
    column_list = []
    can_delete = True
    can_create = False
    can_edit = False

    name = "Driver"
    name_plural = "Drivers"
    icon = "fa-solid fa-driver"


class RepairAdmin(ModelView, model=Repairs):
    column_list = []
    can_delete = True
    can_create = False
    can_edit = False

    name = "Repair"
    name_plural = "Repairs"
    icon = "fa-solid fa-repair"


class TripAdmin(ModelView, model=Trips):
    column_list = []
    can_delete = True
    can_create = False
    can_edit = False

    name = "Trip"
    name_plural = "Trips"
    icon = "fa-solid fa-trip"
