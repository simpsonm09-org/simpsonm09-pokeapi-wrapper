# Pokemon

The wrapper reads Pokemon data from PokeAPI and returns a small shape of its own. It is the one user-facing feature.

## What it does

- `GET /healthz` returns `{"status": "ok"}`. It never calls PokeAPI.
- `GET /pokemon/{name}` returns one Pokemon.
- `GET /pokemon/{name}/encounters` returns the location areas where the Pokemon appears, with the versions it appears in.

`{name}` accepts letters, digits, and hyphens, up to 64 characters. PokeAPI resolves the name case-insensitively.

## Data shape

`GET /pokemon/{name}` returns:

```json
{
  "name": "pikachu",
  "id": 25,
  "types": [{"name": "electric", "slot": 1}],
  "abilities": [
    {"name": "static", "slot": 1, "is_hidden": false},
    {"name": "lightning-rod", "slot": 3, "is_hidden": true}
  ],
  "height": 4,
  "weight": 60
}
```

`GET /pokemon/{name}/encounters` returns a list:

```json
[
  {"location_area": "viridian-forest", "versions": ["red", "blue"]}
]
```

The wrapper maps PokeAPI's nested objects (`type.name`, `ability.name`, `location_area.name`, `version_details[].version.name`) into flat fields. No upstream field is passed through unchanged.

## Failure modes

| Condition | Response |
| --- | --- |
| A name that PokeAPI does not know, so upstream answers 404 | `404` with a `detail` string. |
| Any other upstream error (500, 503, a body that is not JSON) | `502` with a `detail` string. |
| PokeAPI is unreachable, so the connection fails | `502` with a `detail` string. |
| A name with a character outside letters, digits, and hyphens, or longer than 64 characters | `422`, rejected by the path validation before the client runs. |

## Where it lives

`src/pokeapi_wrapper/app.py` holds the routes and the error handlers. `src/pokeapi_wrapper/client.py` holds `PokeApiClient`, which talks to PokeAPI and maps the payload. `src/pokeapi_wrapper/models.py` holds the response models.
