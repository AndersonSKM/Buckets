FROM python:3.6-alpine3.7

# Install packages
RUN apk update && apk upgrade && \
    apk add --update \
    git \
    bash \
    curl \
    python3-dev \
    libffi-dev \
    build-base \
    gettext \
    jpeg-dev \
    zlib-dev

RUN mkdir -p /app
RUN mkdir -p /dist

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app

ENV PYTHONPATH=/app

RUN python3 setup.py sdist
RUN mv dist/* /dist && rm -rf dist/
