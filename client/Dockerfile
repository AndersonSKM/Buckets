FROM cypress/base:8

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

CMD ["yarn", "serve"]
