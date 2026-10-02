"""Response models for the PokeAPI wrapper.

PokeAPI's payloads are mapped into these shapes before they leave the service,
so the upstream JSON never reaches a caller unchanged.
"""

from __future__ import annotations

from pydantic import BaseModel


class Health(BaseModel):
    """Liveness of the service."""

    status: str


class PokemonType(BaseModel):
    """One type slot on a Pokemon."""

    name: str
    slot: int


class Ability(BaseModel):
    """One ability slot on a Pokemon."""

    name: str
    slot: int
    is_hidden: bool


class Pokemon(BaseModel):
    """A Pokemon read from PokeAPI."""

    name: str
    id: int
    types: list[PokemonType]
    abilities: list[Ability]
    height: int
    weight: int


class Encounter(BaseModel):
    """A place a Pokemon appears, with the versions it appears in."""

    location_area: str
    versions: list[str]
