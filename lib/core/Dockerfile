FROM python:3.6-alpine3.7

# Install packages
RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    python3-dev \
    libffi-dev \
    build-base \
    gettext \
    jpeg-dev \
    zlib-dev

# Create dir's
RUN mkdir -p /app
RUN mkdir -p /dist
WORKDIR /app

# Install python dependencies
COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the lib
COPY . /app

ENV PYTHONPATH=/app

RUN python3 setup.py sdist
RUN mv dist/* /dist && rm -rf dist/
