.PHONY: checks
checks:
	pre-commit run --all-files

.PHONY: test
test:
	pytest

.PHONY: venv
venv:
	python -m venv .venv && \
	source .venv/bin/activate && \
	pip install .[dev] && \
	pip install .[project] && \
	pre-commit install
