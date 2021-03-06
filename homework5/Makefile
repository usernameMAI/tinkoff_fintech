TESTS = tests

VENV ?= .venv
CODE = app

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv:
	python -m venv $(VENV)
	$(VENV)/Scripts/python -m pip install --upgrade pip
	$(VENV)/Scripts/python -m pip install poetry
	$(VENV)/Scripts/poetry install
.PHONY: test
test: ## Runs pytest
	$(VENV)/Scripts/pytest -v tests

.PHONY: lint
lint: ## Lint code
	$(VENV)/Scripts/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/Scripts/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/Scripts/mypy $(CODE)
	$(VENV)/Scripts/black --skip-string-normalization --check $(CODE)

.PHONY: format
format: ## Formats all files
	$(VENV)/Scripts/isort $(CODE)
	$(VENV)/Scripts/black --skip-string-normalization $(CODE)
	$(VENV)/Scripts/autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(VENV)/Scripts/unify --in-place --recursive $(CODE)

.PHONY: up
up:	## Runs program
	uvicorn app.app:app --reload --host=0.0.0.0 --port=80 --proxy-headers

.PHONY: up-docker
up-docker:	## Runs program in docker
	docker build -t hw5 .
	docker run -d --name hw5_container -p 80:80 hw5


.PHONY: ci
ci:	lint test ## Lint code then run tests
