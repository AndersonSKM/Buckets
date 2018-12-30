FROM cypress/base:latest

RUN yarn global add cypress@3.1.1

RUN mkdir -p /e2e/
COPY . /e2e/
RUN chmod +x /e2e/run.sh
WORKDIR /e2e/

RUN chmod +x /root/.cache/Cypress/3.1.1/Cypress
RUN chmod +x /e2e/run.sh

CMD ["cypress", "verify"]
