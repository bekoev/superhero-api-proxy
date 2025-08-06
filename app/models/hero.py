from typing import Annotated

from pydantic import BaseModel, BeforeValidator


def is_null(value: int | str | None) -> int | str | None:
    if value is None:
        return None
    if value == "null":
        return None
    return value


class PowerStats(BaseModel):
    intelligence: Annotated[int | None, BeforeValidator(is_null)] = None
    strength: Annotated[int | None, BeforeValidator(is_null)] = None
    speed: Annotated[int | None, BeforeValidator(is_null)] = None
    # durability: Annotated[int | None, BeforeValidator(is_null)] = None
    power: Annotated[int | None, BeforeValidator(is_null)] = None
    # combat: Annotated[int | None, BeforeValidator(is_null)] = None


class Hero(BaseModel):
    id: int
    name: str
    powerstats: PowerStats


class FilterParams(BaseModel):
    name: str | None = None
    intelligenceFrom: int | None = None
    intelligenceTo: int | None = None
    strengthFrom: int | None = None
    strengthTo: int | None = None
    speedFrom: int | None = None
    speedTo: int | None = None
    powerFrom: int | None = None
    powerTo: int | None = None
