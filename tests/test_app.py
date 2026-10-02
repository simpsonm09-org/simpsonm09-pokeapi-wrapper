"""End-to-end tests for the HTTP surface, with PokeAPI stubbed by MockTransport."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi.testclient import TestClient

POKEMON = {
    "name": "pikachu",
    "id": 25,
    "types": [{"name": "electric", "slot": 1}],
    "abilities": [
        {"name": "static", "slot": 1, "is_hidden": False},
        {"name": "lightning-rod", "slot": 3, "is_hidden": True},
    ],
    "height": 4,
    "weight": 60,
}


def ok(payload: Any) -> Any:
    """Build a handler that answers every upstream request with ``payload``."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return handler


def status(code: int) -> Any:
    """Build a handler that answers every upstream request with ``code``."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(code)

    return handler


def test_health_reports_ok(client_factory) -> None:
    client: TestClient = client_factory(ok({}))
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_pokemon_returns_the_wrapper_shape(client_factory, pokemon_payload) -> None:
    client: TestClient = client_factory(ok(pokemon_payload))
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == POKEMON


def test_upstream_404_becomes_our_404(client_factory) -> None:
    client: TestClient = client_factory(status(404))
    response = client.get("/pokemon/missingno")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_upstream_500_becomes_502(client_factory) -> None:
    client: TestClient = client_factory(status(500))
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 502
    assert "detail" in response.json()


def test_invalid_name_is_rejected_with_422(client_factory) -> None:
    client: TestClient = client_factory(ok({}))
    response = client.get("/pokemon/!!!")
    assert response.status_code == 422


def test_encounters_returns_locations(client_factory, encounters_payload) -> None:
    client: TestClient = client_factory(ok(encounters_payload))
    response = client.get("/pokemon/pikachu/encounters")
    assert response.status_code == 200
    assert response.json() == [{"location_area": "viridian-forest", "versions": ["red", "blue"]}]


def test_encounters_upstream_error_becomes_502(client_factory) -> None:
    client: TestClient = client_factory(status(503))
    response = client.get("/pokemon/pikachu/encounters")
    assert response.status_code == 502


def test_openapi_lists_the_endpoints(client_factory) -> None:
    client: TestClient = client_factory(ok({}))
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/pokemon/{name}" in paths
    assert "/pokemon/{name}/encounters" in paths
    assert "/healthz" in paths
