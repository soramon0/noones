FROM python:3.8.3-slim-buster as builder

LABEL maintainer="Soramon" version="0.1"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements ./requirements
RUN pip wheel --no-cache-dir --no-deps --wheel-dir  /usr/src/app/wheels -r requirements/prod.txt

FROM node:14.3 as client-builder

WORKDIR /usr/src/client

COPY ./app/theme/ .
RUN cd static_src \
    && npm install \
    && npm run build:all

FROM python:3.8.3-slim-buster

RUN groupadd --gid 1000 sora \
    && useradd --uid 1000 --gid sora --shell /bin/bash --create-home sora

WORKDIR /home/sora/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=client-builder /usr/src/client/static ./theme/static
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements .
RUN pip install --no-cache /wheels/*

COPY ./app .

RUN chown -R sora:sora /home/sora/app

EXPOSE 8000

USER sora