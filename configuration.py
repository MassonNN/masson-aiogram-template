""" This file represents configurations from files and environment"""
from dataclasses import dataclass
from os import getenv

from sqlalchemy.engine import URL


@dataclass
class Database:
    """ Database connection variables """
    name: str = getenv("POSTGRES_DATABASE")
    user: str = getenv("POSTGRES_USER", "docker")
    passwd: str = getenv("POSTGRES_PASSWORD", "")
    port: int = int(getenv("POSTGRES_PORT", 5432))
    host: str = getenv("POSTGRES_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """
        This function build a connection string
        """
        return URL.create(
            drivername=f"{self.driver}+{self.database_system}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host
        )


@dataclass
class Redis:
    """ Redis connection variables """
    db: str = getenv("REDIS_DATABASE", 1)
    host: str = getenv("REDIS_HOST", "redis")
    port: int = getenv("REDIS_PORT", 6379)
    passwd: int = getenv("REDIS_PASSWORD")
    username: int = getenv("REDIS_USERNAME")
    state_ttl: int = getenv("REDIS_TTL_STATE", None)
    data_ttl: int = getenv("REDIS_TTL_DATA", None)


@dataclass
class Bot:
    """ Bot configuration """
    token: str = getenv("BOT_TOKEN")


@dataclass
class Configuration:
    """ All in one configuration's class """
    db = Database()
    redis = Redis()
    bot = Bot()


conf = Configuration()
