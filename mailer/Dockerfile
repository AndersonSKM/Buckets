FROM python:3.6-alpine3.7

# Install packages
RUN apk update && apk upgrade && \
    apk add --update \
    curl \
    build-base \
    python3-dev \
    libevent-dev

# Create dir's
RUN mkdir -p /app

# Install python dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the app
COPY . /app

# Run nameko services
CMD ["/bin/sh", "/app/run.sh"]