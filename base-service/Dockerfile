FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    git \
    curl \
    bash \
    build-base \
    python3-dev \
    libevent-dev

RUN mkdir -p /app

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

WORKDIR /dist
COPY --from=buckets/service-core:latest /dist/* /dist
RUN pip3 install service_core-0.1.tar.gz

WORKDIR /usr/local/bin
RUN curl -s https://codecov.io/bash > .codecov
RUN chmod +x .codecov
RUN ln -s /usr/local/bin/.codecov codecov
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]
CMD ["nameko shell", "--config=config.yml"]