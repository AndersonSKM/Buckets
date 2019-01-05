#!make
include .env
export $(shell sed 's/=.*//' .env)

PROJECT_NAME := cash-miner

up:
	docker-compose up -d
	make health-check
	make migrate

stop:
	docker-compose stop

build:
	docker-compose build

logs:
	docker-compose logs --follow --tail=40 $(service)

sh:
	docker-compose exec web bash

test: clean pytest flake isort jest eslint cypress

coverage:
	docker-compose exec web bash -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"
	docker-compose exec web bash -c "cd client/ && curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

pytest:
	docker-compose exec web pytest

jest:
	docker-compose exec web yarn --cwd=/app/client/ test:unit

cypress:
	docker-compose run --rm --no-deps cypress bash run.sh

eslint:
	docker-compose exec web yarn --cwd=/app/client/ lint

eslint-fix:
	docker-compose exec web yarn --cwd=/app/client/ lint:fix

flake:
	docker-compose exec web flake8

isort:
	docker-compose exec web isort --check --diff -tc -rc .

fix-imports:
	docker-compose exec web isort -tc -rc .

list-outdated:
	docker-compose exec web pip3 list --outdated --format=columns

clean:
	$(info Cleaning directories)
	@docker-compose exec web sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec web sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec web sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec web sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose exec web sh -c "rm -f .coverage && rm -rf coverage/ && rm -rf client/coverage"

health-check:
	@docker-compose exec web curl \
		-H "Accept: application/json" \
		-sS --retry 10 --retry-max-time 30 --retry-connrefused http://0.0.0.0:8000/api/health-check/

migrate:
	@docker-compose exec web python3 manage.py migrate --noinput

makemigrations:
	@docker-compose exec web python3 manage.py makemigrations

collectstatic:
	@docker-compose exec web python3 manage.py collectstatic --noinput
