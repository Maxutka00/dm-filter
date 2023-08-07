import configparser
from dataclasses import dataclass
from typing import Union

api_id = 5341778
api_hash = "43156e6a67501a046b883b3ef356fc61"
receiver_user_id = 666445915


@dataclass
class UbConfig:
    api_id: int
    api_hash: str


@dataclass
class Config:
    ub: UbConfig
    receiver_user: Union[str, int]


def load_config(path):
    config_file = configparser.ConfigParser()
    config_file.read(path)
    return Config(
        ub=UbConfig(
            **config_file["userbot"]
        ),
        **config_file["other"]
    )


config = load_config("config.ini")
