import hashlib
import uuid

from src.services.redis import redis_client


class Encryption:
    SESSION_EXPIRE_MINUTES = 120

    @classmethod
    def hash(cls, text: str) -> str:
        hash_object = hashlib.sha256(text.encode())
        hash = hash_object.hexdigest()
        return hash

    @classmethod
    def create_token(cls, user_id: str) -> str:
        str = f"{user_id}:{uuid.uuid4()}"
        return cls.hash(str)



