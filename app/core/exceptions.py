from fastapi import HTTPException, status


class AutoException(HTTPException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):

        super().__init__(status_code=self.status_code, detail=self.detail)

class InvalidPriceFilter(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Минимальная цена больше максимальной."


class CarNotFound(AutoException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Автомобиль не найден."


class CarAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Автомобиль уже существует."


class InvalidCarNumber(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный формат номера, пример: Т456КУ"


class UserAlreadyExistsException(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class TokenExpiredException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class NotEnterAccountException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пожалуйста, войдите в аккаунт для выполнения этого действия."


class IncorrectTokenFormatException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED


class AccidentNotFound(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Авария не найдена."


class TripNotFound(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Поездка не найдена."


class DriverNotFound(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Водитель не найден."


class RepairNotFound(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ремонт не найден."


class AccidentAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Авария уже зарегистрирована."


class DriverAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Водитель уже существует."


class RepairAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Ремонт уже зарегистрирован."


class TripAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Поездка уже зарегистрирована."
