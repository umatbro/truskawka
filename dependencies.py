from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer  # type: ignore[import]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Dict[str, str | int] | None:
    if token == "mat":
        return {"id": 1, "username": "Mat"}
    return None
