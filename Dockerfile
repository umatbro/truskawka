FROM python:3.10

WORKDIR /app
RUN pip install poetry
COPY . /app
RUN poetry install --no-dev

ENTRYPOINT poetry run python main.py
