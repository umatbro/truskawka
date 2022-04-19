from functools import lru_cache
from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.engine import Engine
from sqlmodel import create_engine
from strawberry.fastapi import BaseContext

from config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class GraphQLContext(BaseContext):
    def __init__(self, engine: Engine):
        self.engine = engine
        super().__init__()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Dict[str, str | int] | None:
    if token == "mat":
        return {"id": 1, "username": "Mat"}
    return None


@lru_cache()
def get_settings():
    return Settings()


async def db_engine(settings: Settings = Depends(get_settings)) -> Engine:
    return create_engine(settings.database_url)


async def get_graphql_context(
    engine: Engine = Depends(db_engine),
) -> GraphQLContext:
    return GraphQLContext(engine=engine)
