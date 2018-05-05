FROM python:3.6-alpine3.7
LABEL maintainer="anderson.krs95@gmail.com"

# Install packages
RUN apk update && apk upgrade && \
    apk add --update \
    curl \
    bash \
    build-base \
    python3-dev \
    libevent-dev

# Create dir's
RUN mkdir -p /app

# Install python dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -U pip==10.0.1
RUN pip3 install -r requirements.txt

# Copy the app
COPY . /app

# Run nameko services
CMD ["/bin/sh", "/app/run.sh"]