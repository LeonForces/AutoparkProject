from pydantic import BaseModel


class SUserRegister(BaseModel):

    login: str
    password: str


class SUserAuth(BaseModel):

    login: str
    password: str