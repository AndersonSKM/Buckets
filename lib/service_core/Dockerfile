FROM python:3.6-alpine3.7
LABEL maintainer="anderson.krs95@gmail.com"

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    python3-dev \
    build-base \
    libevent-dev

RUN mkdir -p /app
RUN mkdir -p /dist
WORKDIR /app

COPY requirements.txt /app
# hadolint ignore=DL3013
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app

RUN python3 setup.py sdist
RUN mv dist/* /dist && rm -rf dist/