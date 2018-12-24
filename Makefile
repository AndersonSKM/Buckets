#!make
include .env
export $(shell sed 's/=.*//' .env)

PROJECT_NAME := buckets

ifeq ("$(CI)", "true")
	CYPRESS_FLAGS := --record
endif

up:
	docker-compose up -d
	make api-health-check
	make api-migrate

stop:
	docker-compose stop

build: client-build api-build e2e-build

logs:
	docker-compose logs --follow --tail=40 $(service)

sh:
	docker-compose exec $(service) sh

test: api-test client-test e2e-test

coverage:
	docker-compose exec api sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"
	docker-compose exec client sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

# API Commands ----------------------------------------------------------------------------------------------------

api-build:
	docker build ./api/ -t $(PROJECT_NAME)/api:dev

api-test: api-clean api-pytest api-lint

api-pytest:
	docker-compose exec api pytest

api-lint: api-flake api-isort

api-flake:
	docker-compose exec api flake8

api-isort:
	docker-compose exec api isort --check --diff -tc -rc .

api-fix-imports:
	docker-compose exec api isort -tc -rc .

api-outdated:
	docker-compose exec api pip3 list --outdated --format=columns

api-clean:
	$(info Cleaning API directories)
	@docker-compose exec api sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "rm -f .coverage && rm -rf coverage/"

api-health-check:
	@docker-compose exec api curl -sS --retry 10 --retry-max-time 30 --retry-connrefused http://0.0.0.0:8000/api/health-check/

api-migrate:
	@docker-compose exec api python3 manage.py migrate --noinput

api-makemigrations:
	@docker-compose exec api python3 manage.py makemigrations

api-collectstatic:
	@docker-compose exec api python3 manage.py collectstatic --noinput

# Client Commands --------------------------------------------------------------------------

client-build:
	docker build --build-arg api_url=$(VUE_APP_API_URL) ./client/ -t $(PROJECT_NAME)/client:dev

client-test: client-lint client-unit

client-unit:
	docker-compose exec client yarn test:unit

client-lint:
	docker-compose exec client yarn lint

client-lint-fix:
	docker-compose exec client yarn lint:fix

# E2E Commands --------------------------------------------------------------------------

e2e-build:
	docker build ./e2e/ -t $(PROJECT_NAME)/e2e:dev

e2e-test:
	ps -ef | grep Xvfb | grep -v grep | awk '{print $2}' | xargs kill -9
	docker-compose run --rm e2e cypress run $(CYPRESS_FLAGS)
