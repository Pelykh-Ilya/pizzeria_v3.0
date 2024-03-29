
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    dsn: str = "postgresql+asyncpg://user:password@127.0.0.1:5434/db1?async_fallback=True"
    pool_size: int = 10
    pool_max_overflow: int = 10
    echo: bool = False

    class Config:
        env_prefix = "APPLICATION_POSTGRES_"


class APPConfig(BaseSettings):
    postgres: PostgresConfig
    secret_key: SecretStr = SecretStr("secret_key")
    token_lifetime: int = 3600

    class Config:
        env_prefix = "APPLICATION_"


def generate_config() -> APPConfig:
    return APPConfig(postgres=PostgresConfig())
