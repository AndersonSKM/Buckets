FROM cypress/browsers:chrome67-ff57

RUN yarn global add cypress@3.1.1

RUN mkdir -p /e2e/
COPY . /e2e/
WORKDIR /e2e/

CMD ["cypress", "verify"]
