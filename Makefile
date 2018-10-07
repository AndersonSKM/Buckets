PROJECT_NAME := buckets

up:
	docker-compose up -d
	make health-check
	make migrate
	make collectstatic

stop:
	docker-compose stop

build: client-build api-build

api-build:
	docker build ./api/ -t $(PROJECT_NAME)/api:dev

client-build:
	docker build ./client/ -t $(PROJECT_NAME)/client:dev

push-api-image:
	make push image=api:dev

push-client-image:
	make push image=client:dev

push:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
	docker push $(PROJECT_NAME)/$(image)

test: api-test client-test

api-test: clean pytest lint

client-test:
	docker-compose exec client yarn test:unit

api-coverage:
	make codecov container=api

client-coverage:
	make codecov container=client

codecov:
	docker-compose exec $(container) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

pytest:
	docker-compose exec api pytest

lint: flake isort

flake:
	docker-compose exec api flake8

isort:
	docker-compose exec api isort --check --diff -tc -rc .

fix-imports:
	docker-compose exec api isort -tc -rc .

outdated:
	docker-compose exec api pip3 list --outdated --format=columns

clean:
	$(info Cleaning directories)
	@docker-compose exec api sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "rm -f .coverage && rm -rf coverage/"

health-check:
	@docker-compose exec api /bin/sh /app/health-check.sh

migrate:
	@docker-compose exec api python3 manage.py migrate --noinput

makemigrations:
	@docker-compose exec api python3 manage.py makemigrations

collectstatic:
	@docker-compose exec api python3 manage.py collectstatic --noinput

logs:
	docker-compose logs --follow --tail=40 $(t)

sh:
	docker-compose exec $(t) sh
