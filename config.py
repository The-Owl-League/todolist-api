from dataclasses import dataclass

from dataclass_factory import Factory

from yaml import safe_load


@dataclass
class SqliteConfig:
    filename: str


@dataclass
class Config:
    sqlite: SqliteConfig


def load_config():
    with open('config.yml') as fs:
        factory = Factory()
        result = factory.load(safe_load(fs), Config)

    return result


config = load_config()
