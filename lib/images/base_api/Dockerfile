FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    python3-dev \
    libffi-dev \
    postgresql-client \
    postgresql-dev \
    build-base \
    gettext \
    jpeg-dev \
    zlib-dev

RUN mkdir -p /app
RUN mkdir -p /dist
RUN mkdir -p /media
RUN mkdir -p /static

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

WORKDIR /dist
COPY --from=lib/api-core:latest /dist/* /dist
RUN pip3 install core-0.1.tar.gz

WORKDIR /usr/local/bin
RUN curl -s https://codecov.io/bash > .codecov
RUN chmod +x .codecov
RUN ln -s /usr/local/bin/.codecov codecov
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]
CMD ["python3", "manage.py", "shell"]