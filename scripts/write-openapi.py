"""Write the FastAPI OpenAPI document to docs/openapi.json.

Run through `just spec`. The output is deterministic so the CI drift check can
compare it byte-for-byte, and so a hand edit goes red.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "docs" / "openapi.json"

# The package is importable after `just deps`; the source path keeps `just spec`
# working before the editable install.
sys.path.insert(0, str(ROOT / "src"))

from pokeapi_wrapper.app import app


def main() -> None:
    document = app.openapi()
    TARGET.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
