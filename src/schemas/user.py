from pydantic import BaseModel


class UserSchemaForAdd(BaseModel):
    username: str
    password: str

