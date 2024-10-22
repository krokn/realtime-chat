from src.database.models import UserModel
from src.schemas.user import UserSchemaForAdd


class User:

    @staticmethod
    async def create_user_model(
            user_data,
            hash_password: str
    ):
        user_model = UserModel(
            username=user_data.username,
            password=hash_password,
            telegram_id=user_data.telegram_id
        )
        return user_model
