from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.api.dependencies.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.dao.users import UsersDAO
from app.api.dependencies.users.dependencies import get_current_user
from app.models.users import Users
from app.schemas.users import SUserAuth, SUserRegister


router = APIRouter(prefix="/auth", tags=["Auth & Пользователи"])


@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(login=user_data.login)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(login=user_data.login, hashed_password=hashed_password, name=user_data.name, email=user_data.email,
                       telephone=user_data.telephone)


@router.post("/login")
async def login_user(user_data: SUserAuth, response: Response):

    user = await authenticate_user(login=user_data.login, password=user_data.password)

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
