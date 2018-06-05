FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    build-base \
    postgresql-dev \
    zlib-dev \
    jpeg-dev

RUN mkdir -p /app
RUN mkdir -p /media
RUN mkdir -p /static

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY . /app
WORKDIR /app

RUN mv docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint.sh"]

CMD ["python3", "manage.py", "shell"]