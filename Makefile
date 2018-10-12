PROJECT_NAME := buckets

up:
	docker-compose up -d
	make api-health-check
	make api-migrate
	make api-collectstatic

stop:
	docker-compose stop

build: client-build api-build

logs:
	docker-compose logs --follow --tail=40 $(service)

sh:
	docker-compose exec $(service) sh

test: api-test client-test

coverage:
	docker-compose exec api sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

ci-cache-save:
	docker save $(docker history -q $(PROJECT_NAME)/api:dev | grep -v '<missing>') | gzip > ${CACHE_FILE_API}
	docker save $(docker history -q $(PROJECT_NAME)/client:dev | grep -v '<missing>') | gzip > ${CACHE_FILE_CLIENT}

ci-cache-recover:
	if [ -f ${CACHE_FILE_API} ]; then gunzip -c ${CACHE_FILE_API} | docker load; fi
	if [ -f ${CACHE_FILE_CLIENT} ]; then gunzip -c ${CACHE_FILE_CLIENT} | docker load; fi

# API Commands ----------------------------------------------------------------------------------------------------

api-build:
	docker build ./api/ -t $(PROJECT_NAME)/api:dev

api-test: clean pytest lint

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
	$(info Cleaning directories)
	@docker-compose exec api sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose exec api sh -c "rm -f .coverage && rm -rf coverage/"

api-health-check:
	@docker-compose exec api /bin/sh /app/health-check.sh

api-migrate:
	@docker-compose exec api python3 manage.py migrate --noinput

api-makemigrations:
	@docker-compose exec api python3 manage.py makemigrations

api-collectstatic:
	@docker-compose exec api python3 manage.py collectstatic --noinput

# Client Commands --------------------------------------------------------------------------

client-build:
	docker build ./client/ -t $(PROJECT_NAME)/client:dev

client-test: client-unit

client-unit:
	docker-compose exec client yarn test:unit