.PHONY: checks
checks:
	pre-commit run --all-files

.PHONY: test
test:
	pytest

.PHONY: venv
venv:
	python3 -m venv .venv
	.venv/bin/pip install .[dev]
