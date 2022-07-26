from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    is_ng_env: bool = False

    class Config:
        env_file = ".env"
