FROM node:8.12-alpine AS builder

RUN apk update && apk upgrade && \
    apk add --update bash python build-base && \
    yarn global add @vue/cli@3.0.3

RUN mkdir -p /client/
WORKDIR /client/
COPY ./client/package.json /client/
COPY ./client/yarn.lock /client/
RUN yarn install --silent --pure-lockfile

COPY ./client/ /client/
RUN yarn build

FROM python:3.6-alpine3.7

RUN apk update && apk upgrade && \
    apk add --update bash curl build-base postgresql-dev zlib-dev jpeg-dev && \
    pip3 install --upgrade pip && pip3 install pipenv

RUN mkdir -p /app/
WORKDIR /app/
COPY ./api/Pipfile /app
COPY ./api/Pipfile.lock /app
ENV PIPENV_HIDE_EMOJIS=true
ENV PIPENV_NOSPIN=true
RUN pipenv install --system --deploy

COPY ./api /app
COPY --from=builder /api/public/ /app/public/

ENV PORT=8000
ENV DEBUG=false
ENV SECRET_KEY=dumb
ENV DATABASE_URL=postgres://postgres:postgres@host.docker.internal:5432/cash-miner
ENV REDIS_URL=redis://host.docker.internal:6379/1
EXPOSE ${PORT}

RUN python manage.py collectstatic --noinput

CMD ["/bin/bash", "-c", "/usr/local/bin/gunicorn api.wsgi -b 0.0.0.0:$PORT"]
