FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    build-base \
    postgresql-dev \
    zlib-dev \
    jpeg-dev

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

RUN mkdir -p /app
RUN mkdir -p /media
RUN mkdir -p /static

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x /app/run.sh
RUN chmod +x /app/release.sh

ENV PORT=8000
EXPOSE ${PORT}

CMD ["/bin/sh", "/app/run.sh"]
