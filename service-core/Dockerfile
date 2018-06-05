FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    build-base \
    libevent-dev

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

# Just keep container alive for exec tests
ENTRYPOINT ["tail", "-F", "/etc/alpine-release"]