"""Unit tests for the client mapping and error translation."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
import pytest

from pokeapi_wrapper.client import NotFound, PokeApiClient, UpstreamError
from pokeapi_wrapper.config import pokeapi_base_url


def run(coro: Any) -> Any:
    return asyncio.run(coro)


def make_client(handler: Any) -> PokeApiClient:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=pokeapi_base_url())
    return PokeApiClient(http)


def test_get_pokemon_maps_the_payload(pokemon_payload) -> None:
    client = make_client(lambda request: httpx.Response(200, json=pokemon_payload))
    pokemon = run(client.get_pokemon("pikachu"))
    assert pokemon.name == "pikachu"
    assert pokemon.id == 25
    assert [(entry.name, entry.slot) for entry in pokemon.types] == [("electric", 1)]
    assert [(entry.name, entry.slot, entry.is_hidden) for entry in pokemon.abilities] == [
        ("static", 1, False),
        ("lightning-rod", 3, True),
    ]
    assert (pokemon.height, pokemon.weight) == (4, 60)


def test_get_pokemon_requests_the_expected_path(pokemon_payload) -> None:
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.url.path)
        return httpx.Response(200, json=pokemon_payload)

    run(make_client(handler).get_pokemon("pikachu"))
    assert seen == ["/api/v2/pokemon/pikachu"]


def test_get_pokemon_raises_not_found() -> None:
    client = make_client(lambda request: httpx.Response(404))
    with pytest.raises(NotFound):
        run(client.get_pokemon("missingno"))


def test_get_pokemon_raises_upstream_error_on_500() -> None:
    client = make_client(lambda request: httpx.Response(500))
    with pytest.raises(UpstreamError):
        run(client.get_pokemon("pikachu"))


def test_get_encounters_maps_the_payload(encounters_payload) -> None:
    client = make_client(lambda request: httpx.Response(200, json=encounters_payload))
    encounters = run(client.get_encounters("pikachu"))
    assert [entry.location_area for entry in encounters] == ["viridian-forest"]
    assert encounters[0].versions == ["red", "blue"]


def test_connection_error_becomes_upstream_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    client = make_client(handler)
    with pytest.raises(UpstreamError):
        run(client.get_pokemon("pikachu"))
