build:
	@docker build . -t lib/core:latest

test: clean unit-test lint

unit-test:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest pytest

lint: flake isort

sh:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh

flake:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest flake8 --exclude=*settings.py,*migrations

isort:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest isort --check --diff -tc -rc .

fix-imports:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest isort -tc -rc .

clean:
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "find . -name "*.pyo" | xargs rm -rf"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "find . -name "*.cache" | xargs rm -rf"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "find . -name "*.mypy_cache" | xargs rm -rf"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "find . -name "*.egg-info" -type d | xargs rm -rf"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "find . -name "__pycache__" -type d | xargs rm -rf"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "rm -f .coverage"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "rm -rf coverage/"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "rm -rf dist/"
	@docker run --rm -it -v $(CURDIR):/app lib/core:latest sh -c "rm -f *.log"

cov:
	@docker run --env-file ./env --rm -it -v $(CURDIR):/app lib/core:latest sh -c "curl -s https://codecov.io/bash > .codecov && chmod +x .codecov && ./.codecov -y ./codecov.yml"