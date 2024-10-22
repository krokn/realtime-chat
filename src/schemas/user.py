from pydantic import BaseModel, Field


class UserSchemaForLogin(BaseModel):
    username: str = Field(..., description="Имя пользователя, которое будет использоваться для входа")
    password: str = Field(..., description="Пароль для учетной записи, должен быть безопасным")


class UserSchemaForAdd(UserSchemaForLogin):
    telegram_id: int = Field(..., description="Уникальный идентификатор пользователя в Telegram для отправки уведомлений")