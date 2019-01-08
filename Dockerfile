FROM node:8.12-alpine AS builder

RUN apk update && apk upgrade && \
    apk add --update \
        bash \
        python \
        build-base

RUN yarn global add @vue/cli@3.0.3

RUN mkdir -p /client/
WORKDIR /client/

COPY ./client/package.json /client/
COPY ./client/yarn.lock /client/
RUN yarn install --silent --pure-lockfile

ADD ./client /client/
RUN yarn build


FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update \
    bash \
    build-base \
    postgresql-dev \
    zlib-dev \
    jpeg-dev

RUN mkdir -p /app/
WORKDIR /app/

RUN pip3 install --upgrade pip && pip3 install pipenv

COPY ./api/Pipfile /app
COPY ./api/Pipfile.lock /app

RUN pipenv install --system --deploy

COPY ./api /app
RUN chmod +x /app/deployment-tasks.sh
COPY --from=builder /api/public/ /app/public/

ENV PORT=8000
ENV DEBUG=false

EXPOSE ${PORT}

CMD ["/bin/bash", "-c", "/usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:$PORT"]
