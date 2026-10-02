# pokeapi-wrapper

A FastAPI service that wraps the public [PokeAPI](https://pokeapi.co/docs/v2). It reads a Pokemon or its encounters upstream and returns a small, stable shape of its own, so a caller never depends on PokeAPI's payload.

The original lives in `simpsonm09-org/simpsonm09-pokeapi-wrapper`; work happens on the personal fork. See [`repo-standard`](https://github.com/simpsonm09-org/simpsonm09-repo-standard).

## What it does

`GET /pokemon/{name}` returns the Pokemon's name, id, types, abilities, height, and weight. `GET /pokemon/{name}/encounters` returns the location areas where it appears. `GET /healthz` reports liveness. PokeAPI is an external boundary, so an upstream 404 becomes the wrapper's 404 and any other upstream failure becomes a 502.

## Quick start

```bash
just install
just deps
just serve
```

Then open <http://127.0.0.1:8000/docs>.

With Docker:

```bash
docker build -t pokeapi-wrapper:local .
docker run --rm -p 8000:8000 pokeapi-wrapper:local
```

## Commands

| Command | Does |
| --- | --- |
| `just install` | Installs the pinned tools. |
| `just deps` | Installs the Python dependencies. |
| `just lint` | Runs the linters. |
| `just test` | Runs the test suite. |
| `just coverage` | Runs the suite with an lcov report under `coverage/`. |
| `just spec` | Regenerates `docs/openapi.json` from the app. |
| `just verify` | Lints and tests. |
| `just serve` | Serves the wrapper on port 8000. |

## Documentation

Read [`docs/README.md`](docs/README.md).

## License

MIT. See [`LICENSE`](LICENSE).

## Related repositories

- [`repo-standard`](https://github.com/simpsonm09-org/simpsonm09-repo-standard) owns the shared CI, linting, security, and governance.
