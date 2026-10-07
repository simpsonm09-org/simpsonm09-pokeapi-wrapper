"""Tests for the PokeAPI base URL configuration."""

from __future__ import annotations

import pytest

from pokeapi_wrapper.config import BASE_URL_ENV, pokeapi_base_url


def test_default_base_url_is_the_public_pokeapi() -> None:
    assert pokeapi_base_url() == "https://pokeapi.co/api/v2/"


def test_base_url_reads_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(BASE_URL_ENV, "http://127.0.0.1:9/")
    assert pokeapi_base_url() == "http://127.0.0.1:9/"
