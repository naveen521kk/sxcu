# Contributing

Please open an new issue for feature requests and mark your interest on any issue open before working on it.

### Development Environment
#### Poetry
This project uses [Poetry](https://python-poetry.org/docs/) for management. You need to have `poetry` installed and
available in your environment.

```sh
pip install --user pipx
pipx install poetry
```

#### Setup development environment
```sh
poetry install
```

#### Activating virtual environment

##### Using poetry
```sh
poetry shell
```

##### Manually

```sh
# Option 1: Use poetry to get the env path
source `poetry env info -p`/bin/activate

# Option 2: If using in-project environments
source .venv/bin/activate
```

**Note:** The use of `poetry run` in the following commands can be skipped if your environment is  already activated.

#### Lint your code

This project is configured using pre-commit.

```sh
poetry run pre-commit install
poetry run pre-commit run --all-files
```

#### Run test suite
This project uses Pytest for testing.
```sh
poetry run pytest
```
