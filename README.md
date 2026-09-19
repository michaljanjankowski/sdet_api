# sdet_api

Examples of API testing solutions.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
uv sync
```

The project uses Python 3.10 or newer. `uv sync` installs the dependencies from
`uv.lock` into `.venv`, including the test dependencies.

## Tests

```sh
uv run python -m pytest
```

The API test example imports `product_source_code`, which must be supplied by the
API under test. Its fixtures also expect that API to be running at the address
configured in `api_test_example/utils/cons.py`.
