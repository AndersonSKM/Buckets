FROM cypress/base:latest

RUN yarn global add cypress@3.1.1

RUN mkdir -p /e2e/
COPY . /e2e/
RUN chmod +x /e2e/run.sh
WORKDIR /e2e/

CMD ["cypress", "verify"]
