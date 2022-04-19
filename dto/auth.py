from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import constr


class CreateUserRequest(BaseModel):
    username: constr(max_length=255)
    password: SecretStr
