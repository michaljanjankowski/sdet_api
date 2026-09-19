# sdet_api

Runnable Python examples for backend SDETs. The API test suite starts an in-memory
HTTP server on a local port, so no external service or credentials are needed.

## Setup and test

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and use
Python 3.10 or newer:

```sh
uv sync --locked
uv run --locked python -m pytest -q
```

| Directory | What it demonstrates | Run it |
| --- | --- | --- |
| `api_test_example/` | API client, typed resource agent, fixtures with cleanup, CRUD, validation, pagination, 401 and 403 responses | `uv run python -m pytest api_test_example -q` |
| `mocking_example/` | Injecting an HTTP session and checking a request without network access | `uv run python -m pytest mocking_example -q` |
| `api_wrapping_example/` | Parsing an external API response and testing the wrapper with a mock session | `uv run python -m pytest api_wrapping_example -q` |

The optional live wrapper requires an API Ninjas key:

```sh
API_ANIMALS_KEY=your-key uv run python -m api_wrapping_example.api_wrapper cat
```

The tests never call that external API.
