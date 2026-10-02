"""An async client for PokeAPI that maps payloads to the wrapper's own models."""

from __future__ import annotations

from typing import Any

import httpx

from .models import Ability, Encounter, Pokemon, PokemonType

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"


class PokeApiError(Exception):
    """Base class for a failure talking to PokeAPI."""


class NotFound(PokeApiError):
    """PokeAPI has no resource for the requested name."""


class UpstreamError(PokeApiError):
    """PokeAPI is unreachable or answered with an error."""


class PokeApiClient:
    """Wrap an ``httpx.AsyncClient`` bound to the PokeAPI base URL."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def _get(self, path: str) -> Any:
        try:
            response = await self._client.get(path)
        except httpx.RequestError as error:
            raise UpstreamError("PokeAPI is unreachable") from error
        if response.status_code == httpx.codes.NOT_FOUND:
            raise NotFound(f"PokeAPI has no resource at {path}")
        if response.status_code >= httpx.codes.BAD_REQUEST:
            raise UpstreamError(f"PokeAPI returned {response.status_code}")
        try:
            return response.json()
        except ValueError as error:
            raise UpstreamError("PokeAPI returned a body that is not JSON") from error

    async def get_pokemon(self, name: str) -> Pokemon:
        """Return the Pokemon named ``name`` in the wrapper's shape."""
        data = await self._get(f"pokemon/{name}")
        return Pokemon(
            name=data["name"],
            id=data["id"],
            height=data["height"],
            weight=data["weight"],
            types=[
                PokemonType(name=entry["type"]["name"], slot=entry["slot"])
                for entry in data["types"]
            ],
            abilities=[
                Ability(
                    name=entry["ability"]["name"],
                    slot=entry["slot"],
                    is_hidden=entry["is_hidden"],
                )
                for entry in data["abilities"]
            ],
        )

    async def get_encounters(self, name: str) -> list[Encounter]:
        """Return where the Pokemon named ``name`` can be encountered."""
        data = await self._get(f"pokemon/{name}/encounters")
        return [
            Encounter(
                location_area=entry["location_area"]["name"],
                versions=[
                    detail["version"]["name"] for detail in entry["version_details"]
                ],
            )
            for entry in data
        ]
