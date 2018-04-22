FROM python:3.6-alpine3.7

# Install packages
RUN apk update && apk upgrade && \
    apk add --update \
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
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /dist
COPY --from=lib/core:latest /dist/* /dist
RUN pip3 install core-0.1.tar.gz

# Copy the app
WORKDIR /app
COPY . /app

RUN chmod ug+x run.sh

CMD ["/bin/sh", "/app/run.sh"]
