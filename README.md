# Hello strawberry project

## Installing dependencies

Project uses poetry to manage dependencies.
```
# activate venv
pip install poetry
python -m poetry install
```

## Running the project

Copy the `.env_example` file to `.env` - this is a file used as a config.
```
cp .env_example .env
```

Run PostgreSQL and the app:
```
docker compose up -d
alembic upgrade head
python main.py
```
