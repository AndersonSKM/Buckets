PROJECT_NAME := buckets

PYTHON_LIBRARIES := service-core
PYTHON_SERVICES := api
PYTHON_IMAGES := $(PYTHON_LIBRARIES) $(PYTHON_SERVICES)
CUSTOM_SERVICES := nginx
BASE_IMAGES := base-service

IMAGES := $(PYTHON_LIBRARIES) $(BASE_IMAGES) $(PYTHON_SERVICES) $(CUSTOM_SERVICES)

up:
	docker-compose up

up-d:
	docker-compose up -d

stop:
	docker-compose stop

build:
	for image in $(IMAGES) ; do \
		echo Building $$image; \
		docker build ./$$image/ -t $(PROJECT_NAME)/$$image:dev || exit 1; \
	done

test: clean unit-test lint

test-all:
	for service in $(PYTHON_IMAGES) ; do \
		make test t=$$service || exit 1; \
	done

coverage:
	for service in $(PYTHON_IMAGES) ; do \
		make codecov t=$$service || exit 1; \
	done

unit-test:
	docker-compose exec $(t) pytest

lint: flake isort

logs:
	docker-compose logs $(t)

flake:
	docker-compose exec $(t) flake8

isort:
	docker-compose exec $(t) isort --check --diff -tc -rc .

fix-imports:
	docker-compose exec $(t) isort -tc -rc .

sh:
	docker-compose exec $(t) sh

outdated:
	docker-compose exec (t) pip3 list --outdated --format=columns

clean:
	$(info Cleaning directories)
	@docker-compose exec $(t) sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose exec $(t) sh -c "rm -f .coverage && rm -rf coverage/"

codecov:
	docker-compose exec $(t) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

deploy:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
	for image in $(IMAGES) ; do \
		docker tag $(PROJECT_NAME)/$$image:dev $(PROJECT_NAME)/$$image:$(TAG) || exit 1; \
		docker push $(PROJECT_NAME)/$$image:$(TAG) || exit 1 ; \
	done