from fastapi import APIRouter, Response, Query

from app.core.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.api.dependencies.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.dao.users import UsersDAO

from typing import Annotated


router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register_user(login: Annotated[str, Query(example="kunzhut", description="Логин")],
                        password: Annotated[str, Query(example="1234", description="Пароль")],
                        name: Annotated[str, Query(example="Kunzhut", description="Имя")],
                        email: Annotated[str, Query(example="vuz@mai.ru", description="Почта")],
                        telephone: Annotated[str, Query(example="+79257797710", description="Номер телефона")]):
    existing_user = await UsersDAO.find_one_or_none(login=login)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(password)
    await UsersDAO.add(login=login, hashed_password=hashed_password, name=name, email=email,
                       telephone=telephone)
    return "Success"


@router.post("/login")
async def login_user(login: Annotated[str, Query(example="kunzhut", description="Логин")],
                     password: Annotated[str, Query(example="1234", description="Пароль")],
                     response: Response):

    user = await authenticate_user(login=login, password=password)

    if not user:

        raise IncorrectEmailOrPasswordException

    access_token = create_access_token(
        {"sub": str(user.id)}
    )
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):

    response.delete_cookie("access_token")


# @router.get("/me")
# async def read_user_me(user: Users = Depends(get_current_user)):
#
#     return user
