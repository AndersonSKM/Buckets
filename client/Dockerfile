FROM cypress/base:8

RUN yarn global add @vue/cli@3.0.3

RUN mkdir -p /client
WORKDIR /client
COPY package.json /client
COPY yarn.lock /client
RUN yarn install --silent --pure-lockfile

COPY . /client

EXPOSE 8080

CMD ["yarn", "serve"]
