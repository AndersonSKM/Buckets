FROM python:3.6-alpine3.7
LABEL maintainer="anderson.krs95@gmail.com"

# Install packages
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

# Create dir's
RUN mkdir -p /app
RUN mkdir -p /dist
RUN mkdir -p /media
RUN mkdir -p /static

# Install python dependencies
WORKDIR /app
COPY requirements.txt /app
# hadolint ignore=DL3013
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install core lib
WORKDIR /dist
COPY --from=lib/api-core:latest /dist/* /dist
RUN pip3 install core-0.1.tar.gz

# Copy the app
WORKDIR /app
COPY . /app

RUN chmod ug+x run.sh

CMD ["/bin/sh", "/app/run.sh"]
