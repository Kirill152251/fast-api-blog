from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn 
    JWT_ALG: str
    JWT_EXP_MIN: int
    JWT_SECRET: str

settings = Config()

