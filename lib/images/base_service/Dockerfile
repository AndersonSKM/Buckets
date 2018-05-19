FROM python:3.6-alpine3.7
LABEL maintainer="anderson.krs95@gmail.com"

RUN apk update && apk upgrade && \
    apk add --update \
    curl \
    bash \
    build-base \
    python3-dev \
    libevent-dev

RUN mkdir -p /app
WORKDIR /app

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

COPY docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]
CMD ["nameko shell", "--config=config.yml"]