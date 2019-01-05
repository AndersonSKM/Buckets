FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    curl \
    build-base \
    postgresql-dev \
    zlib-dev \
    jpeg-dev \
    nodejs \
    yarn \
    python

RUN mkdir -p /app
RUN mkdir -p /app/client/
RUN mkdir -p /app/media/
RUN mkdir -p /app/public/

RUN yarn global add @vue/cli@3.0.3

WORKDIR /tmp
COPY client/package.json /tmp
COPY client/yarn.lock /tmp
RUN yarn install --silent --pure-lockfile
RUN cp -R /tmp/node_modules /app/client/node_modules/

RUN pip3 install --upgrade pip

COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app
RUN yarn --cwd=/app/client/ build
RUN chmod +x /app/run.sh

ENV PORT=8000
ENV NODE_PORT=8080
EXPOSE ${PORT}

CMD ["/bin/bash", "/app/run.sh"]
