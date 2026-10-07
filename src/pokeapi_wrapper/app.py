"""The FastAPI application that exposes reads over PokeAPI."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, Path, Request
from fastapi.responses import JSONResponse

from .client import NotFound, PokeApiClient, UpstreamError
from .config import pokeapi_base_url
from .models import Encounter, Health, Pokemon


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Build one upstream client for the process and close it on shutdown."""
    async with httpx.AsyncClient(base_url=pokeapi_base_url(), timeout=10.0) as http:
        app.state.client = PokeApiClient(http)
        yield


app = FastAPI(title="PokeAPI Wrapper", version="0.1.0", lifespan=lifespan)


def get_client(request: Request) -> PokeApiClient:
    """Return the client built at startup. Tests override this dependency."""
    return request.app.state.client


@app.exception_handler(NotFound)
async def handle_not_found(request: Request, exc: NotFound) -> JSONResponse:
    """Map an upstream 404 to the wrapper's own 404."""
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(UpstreamError)
async def handle_upstream_error(request: Request, exc: UpstreamError) -> JSONResponse:
    """Map any other upstream failure to a 502."""
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/healthz", response_model=Health)
async def health() -> Health:
    return Health(status="ok")


@app.get("/pokemon/{name}", response_model=Pokemon)
async def read_pokemon(
    name: str = Path(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9-]+$"),
    client: PokeApiClient = Depends(get_client),
) -> Pokemon:
    return await client.get_pokemon(name)


@app.get("/pokemon/{name}/encounters", response_model=list[Encounter])
async def read_encounters(
    name: str = Path(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9-]+$"),
    client: PokeApiClient = Depends(get_client),
) -> list[Encounter]:
    return await client.get_encounters(name)
