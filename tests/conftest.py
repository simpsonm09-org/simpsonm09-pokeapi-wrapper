from __future__ import annotations

import json
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from pokeapi_wrapper.app import app, get_client
from pokeapi_wrapper.client import POKEAPI_BASE_URL, PokeApiClient

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def pokemon_payload() -> Any:
    return _load("pokemon_pikachu.json")


@pytest.fixture
def encounters_payload() -> Any:
    return _load("encounters_pikachu.json")


@pytest.fixture
def client_factory() -> Iterator[Callable[[httpx.MockTransport], TestClient]]:
    """Build a TestClient whose upstream is stubbed by a MockTransport handler."""

    def make(handler: Callable[[httpx.Request], httpx.Response]) -> TestClient:
        http = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url=POKEAPI_BASE_URL)
        client = PokeApiClient(http)
        app.dependency_overrides[get_client] = lambda: client
        return TestClient(app)

    yield make
    app.dependency_overrides.clear()
