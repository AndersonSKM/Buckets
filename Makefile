PROJECT := buckets

PYTHON_LIBRARIES := api-core service-core
PYTHON_APIS := auth
PYTHON_IMAGES := $(PYTHON_LIBRARIES) $(PYTHON_APIS)
BASE_IMAGES := base-api base-service
CUSTOM_SERVICES := nginx

IMAGES := $(PYTHON_LIBRARIES) $(BASE_IMAGES) $(PYTHON_APIS) $(CUSTOM_SERVICES)

define command
	$(if $(filter $(1),$(PYTHON_LIBRARIES)),run --rm --no-deps,exec) $(1)
endef

up:
	docker-compose up

up-d:
	docker-compose up -d

stop:
	docker-compose stop

build:
	for image in $(IMAGES) ; do \
		echo Building $$image; \
		docker build ./$$image/ -t $(PROJECT)/$$image:latest; \
	done

test: clean unit-test lint

test-all:
	for service in $(PYTHON_IMAGES) ; do \
		make test t=$$service; \
	done

coverage:
	for service in $(PYTHON_IMAGES) ; do \
		make codecov t=$$service; \
	done

unit-test:
	docker-compose $(call command,$(t)) pytest

lint: flake isort

logs:
	docker-compose logs $(t)

flake:
	docker-compose $(call command,$(t)) flake8

isort:
	docker-compose $(call command,$(t)) isort --check --diff -tc -rc .

fix-imports:
	docker-compose $(call command,$(t)) isort -tc -rc .

sh:
	docker-compose $(call command,$(t)) sh

outdated:
	docker-compose $(call command,$(t)) pip3 list --outdated --format=columns

clean:
	$(info Cleaning directories)
	@docker-compose $(call command,$(t)) sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose $(call command,$(t)) sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose $(call command,$(t)) sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose $(call command,$(t)) sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose $(call command,$(t)) sh -c "find . -name ".pytest_cache" -type d | xargs rm -rf"
	@docker-compose $(call command,$(t)) sh -c "rm -f .coverage && rm -rf coverage/"

codecov:
	docker-compose $(call command,$(t)) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov"

deploy:
	docker login -e $(DOCKER_EMAIL) -u $(DOCKER_USER) -p $(DOCKER_PASS)
	for image in $(IMAGES) ; do \
		docker tag $(PROJECT)/$$image:latest $(PROJECT)/:$(TAG); \
		docker push $(PROJECT)/$$image; \
	done