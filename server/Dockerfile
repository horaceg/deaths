FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/

RUN pip install -U pip && pip install -Ur requirements.txt

COPY ./app /app
COPY ./data /app/data
