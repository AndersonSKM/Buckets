up:
	@docker-compose up

up-d:
	@docker-compose up -d

stop:
	@docker-compose stop

build:
	$(MAKE) -C lib/core build
	@docker-compose build

test: clean unit-test lint

test-all:
	$(MAKE) -C lib/core test
	$(MAKE) test t=auth

unit-test:
	@docker-compose exec $(t) pytest

lint: flake isort

logs:
	@docker-compose logs $(t)

flake:
	@docker-compose exec $(t) flake8 --exclude=*settings.py,*test_settings.py,*manage.py,*migrations

isort:
	@docker-compose exec $(t) isort --check --diff -tc -rc .

fix-imports:
	@docker-compose exec $(t) isort -tc -rc .

sh:
	@docker-compose exec $(t) sh

sync-db:
	@docker-compose exec $(t) sh -c "python3 manage.py makemigrations && python3 manage.py migrate"

outdated:
	@docker-compose exec $(t) sh -c "pip3 list --outdated --format=columns"

clean:
	@docker-compose exec $(t) sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker-compose exec $(t) sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker-compose exec $(t) sh -c "rm -f .coverage"
	@docker-compose exec $(t) sh -c "rm -rf coverage/"

cov:
	@docker-compose exec $(ci_env) $(t) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov"

coverage:
	$(MAKE) -C lib/core cov ci_env=$(ci_env)
	$(MAKE) cov t=auth ci_env=$(ci_env)
