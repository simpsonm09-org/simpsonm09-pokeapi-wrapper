# pokeapi-wrapper working agreements

A FastAPI service that wraps the public PokeAPI and returns a small shape of its own.

## Ground rules

- PokeAPI is an external boundary; mock it in tests. Never call the real PokeAPI from a test.
- Do not leak PokeAPI's payload shape through a response. Map it to the models in `src/pokeapi_wrapper/models.py`.
- `docs/openapi.json` is generated. Run `just spec`; never hand-edit it.
- No secret, credential, or machine path is committed.

## Commands

- `just install`, `just deps`, `just lint`, `just test`, `just coverage`, `just spec`, `just verify`.
- `just serve` runs the service on <http://127.0.0.1:8000>.

## Repo facts

- Language and toolchain: Python 3.12, FastAPI, pydantic v2, httpx, uvicorn, pinned in `mise.toml` and `pyproject.toml`.
- Data: no database. State is per request; one shared `httpx.AsyncClient` is built at startup and closed at shutdown.
- Domain: the routes map names to their models through `PokeApiClient`. An upstream 404 becomes the wrapper's 404 and any other upstream error becomes a 502.
- Docs: `docs/README.md` indexes the architecture, the Pokemon feature, and the OpenAPI contract.

## Skills

No repo-local skills. General best practices and integration come from the plugins.
