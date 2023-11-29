from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    RedisStrategy,
)
from redis import asyncio as redis_async

from src import config
from src.auth.models import UserModel
from src.auth.utils import get_user_manager

cookie_transport = CookieTransport(cookie_name="financier_auth", cookie_max_age=3600)
redis = redis_async.from_url(config.REDIS_URL, encoding="utf8", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
