SERVICES := api_core service_core auth

define command
	$(if $(filter $(1),api_core service_core),run --rm --no-deps, exec) $(1)
endef

up:
	docker-compose up

up-d:
	docker-compose up -d

stop:
	docker-compose stop

build:
	docker build ./lib/api_core -t lib/api-core:latest
	docker build ./lib/service_core -t lib/service-core:latest
	docker build ./lib/images/base_service -t lib/base-service:latest
	docker-compose build

test: clean unit-test lint

test-all:
	make test t=api_core
	make test t=service_core
	make test t=auth

coverage:
	make codecov t=api_core
	make codecov t=service_core
	make codecov t=auth

unit-test:
	docker-compose $(call command,$(t)) pytest

lint: flake isort

logs:
	docker-compose logs $(t)

flake:
	docker-compose $(call command,$(t)) flake8 --exclude=*settings.py,*test_settings.py,*manage.py,*migrations

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
	docker-compose $(call command,$(t)) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"
