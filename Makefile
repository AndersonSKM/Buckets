#!make

test: clean pytest flake isort jest eslint cypress

coverage:
	curl -s https://codecov.io/bash > .codecov
	chmod +x .codecov
	./.codecov -Z api/
	./.codecov -Z client/

pytest:
	cd api/ && pytest

jest:
	yarn --cwd=./client/ test:unit

cypress:
	yarn --cwd=./client/ test:e2e

eslint:
	yarn --cwd=./client/ lint

eslint-fix:
	yarn --cwd=./client/ lint:fix

flake:
	flake8 api/

isort:
	isort --check --diff -tc -rc api/

fix-imports:
	isort -tc -rc api/

list-outdated:
	cd api/
	pip3 list --outdated --format=columns

clean:
	$(info Cleaning directories)
	find api/ -name "*.pyo" | xargs rm -rf
	find api/ -name "*.cache" | xargs rm -rf
	find api/ -name "__pycache__" -type d | xargs rm -rf
	find api/ -name ".pytest_cache" -type d | xargs rm -rf
	rm -f api/.coverage
	rm -rf api/public/*.*
	rm -rf api/coverage/
	rm -rf client/coverage/

health-check:
	curl \
		-H "Accept: application/json" \
		-sS --retry 10 --retry-max-time 30 --retry-connrefused http://0.0.0.0:8000/api/health-check/
