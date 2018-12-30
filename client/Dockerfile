FROM node:8.12-alpine

RUN apk update && apk upgrade && \
    apk add --update \
        python \
        curl \
        bash \
        build-base

RUN yarn global add @vue/cli@3.0.3

WORKDIR /tmp
COPY package.json /tmp
COPY yarn.lock /tmp
RUN yarn install --silent --pure-lockfile

RUN mkdir -p /client
WORKDIR /client
RUN cp -R /tmp/node_modules /client/

COPY . /client

EXPOSE 8080

ARG api_url
ENV VUE_APP_API_URL=$api_url

RUN yarn build

CMD ["yarn", "serve"]
