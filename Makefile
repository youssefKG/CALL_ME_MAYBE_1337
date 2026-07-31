UV := uv
PYTHON := $(UV) run python
PROJECT := src


install: 
	$(UV) sync --all-packages

run:
	$(PYTHON) -m $(PROJECT)

debug:
	$(UV) run python -m pdb src/__main__.py


clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	rm -rf .venv *.egg-info

lint:
	$(UV) run flake8 $(PROJECT)
	$(UV) run mypy $(PROJECT) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
	$(UV) run mypy $(PROJECT) --strict
	$(UV) run flake8 $(PROJECT)

.PHONY: install run debug clean lint lint-strict
