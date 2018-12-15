FROM node:8.12-slim

RUN apt-get update && \
    apt-get install -y \
        libgtk2.0-0 \
        libnotify-dev \
        libgconf-2-4 \
        libnss3 \
        libxss1 \
        libasound2 \
        xvfb \
        build-essential

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
