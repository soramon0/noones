# TODO(karim): refactor this for production
FROM python:3.8.3-slim-buster

LABEL maintainer="Soramon" version="0.1"

RUN groupadd --gid 1000 sora \
    && useradd --uid 1000 --gid sora --shell /bin/bash --create-home sora

WORKDIR /home/sora/app
COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY ./app .

RUN chown -R sora:sora /home/sora/app

EXPOSE 8000

USER sora