from pydantic import BaseModel


class UserSchemaForAdd(BaseModel):
    username: str
    password: str
    telegram_id: int


class UserSchemaForLogin(BaseModel):
    username: str
    password: str

