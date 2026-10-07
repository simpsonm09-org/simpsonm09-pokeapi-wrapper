"""Runtime configuration for the wrapper, read from the environment."""

from __future__ import annotations

import os

BASE_URL_ENV = "POKEAPI_BASE_URL"


def pokeapi_base_url() -> str:
    """Return the PokeAPI base URL, defaulting to the public API."""
    return os.environ.get(BASE_URL_ENV, "https://pokeapi.co/api/v2/")
