PROJECT_NAME := buckets
IMAGES := api nginx postgres redis

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

logs:
	docker-compose logs $(t)

sh:
	docker-compose exec $(t) sh

deploy:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
	for image in $(IMAGES) ; do \
		docker tag $(PROJECT_NAME)/$$image:dev $(PROJECT_NAME)/$$image:$(TAG) || exit 1; \
		docker push $(PROJECT_NAME)/$$image:$(TAG) || exit 1 ; \
	done

test: clean pytest lint

coverage:
	make codecov t=api

codecov:
	docker-compose exec $(t) sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -Z"

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
