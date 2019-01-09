#!make

clean:
	$(info Cleaning directories)
	@find api/ -name "*.pyo" | xargs rm -rf
	@find api/ -name "*.cache" | xargs rm -rf
	@find api/ -name "__pycache__" -type d | xargs rm -rf
	@find api/ -name "*.pytest_cache" -type d | xargs rm -rf
	@find api/ -name "*.coverage" | xargs rm -rf
	@find api/ -name "coverage.xml" | xargs rm -rf
	@rm -rf api/coverage/
	@rm -rf client/coverage/
	@rm -rf client/tests/e2e/videos/
	@rm -rf client/tests/e2e/screenshots/
	@find client/ -name "yarn-error.log" | xargs rm -rf
	@find client/ -name "*.Trash-0" | xargs rm -rf

health-check:
	$(info Performing System Check)
	@curl -H "Accept: application/json" \
    	-sS --retry 10 --retry-max-time 30 \
        --retry-connrefused http://0.0.0.0:8000/api/health-check/

build:
	$(info Building docker image)
	docker build . -t cash-miner:dev -f Dockerfile

deploy-local:
	$(info Running image localy)
	docker run --rm -p 8000:8000 \
		-e DATABASE_URL \
		-e REDIS_URL \
		-e SECRET_KEY \
		-it --name cash-miner cash-miner:dev \

codecov:
	$(info Running test coverage)
	curl -s https://codecov.io/bash > .codecov
	chmod +x .codecov
	./.codecov -Z api/
	./.codecov -Z client/
