PYTHON = python3
VENV = .venv

REQUIREMENT = requirement.txt

VENV_BIN = $(VENV)/bin

PYTHON_PATH = $(VENV_BIN)/python

PIP_PATH = $(VENV_BIN)/pip

RM = rm

RM_FLAGS = -rf

CACHE = ./__pycache__ .mypy_cache .flake8

DEFAULT_MAP = ./maps/challenger/01_the_impossible_dream.txt

FILES = ./Graph.py Log.py ./Path.py ./Interfaces.py  ./Errors.py ./Parser.py \
				./Enums.py  ./Dijkstra.py ./Colors.py ./Simulation.py  ./Validator.py \
				./FileReader.py ./Singleton.py ./Mettadata.py ./main.py ./GraphBuilder.py

MAIN = main.py

MYPY = mypy
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs

run: env 
	$(PYTHON_PATH) $(MAIN) $(DEFAULT_MAP)
env: # create virtual enviroment
	@if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi

install: env
	@$(PIP_PATH) install -r $(REQUIREMENT)


lint: env
	@$(PYTHON_PATH) -m $(MYPY) $(FILES) $(MYPY_FLAGS)
	@$(PYTHON_PATH) -m flake8 $(FILES)

clean:
	$(RM) $(RM_FLAGS)  $(CACHE)
	$(RM) $(RM_FLAGS) $(VENV)

debug:
	$(PYTHON_PATH) -m pdb $(MAIN) $(DEFAULT_MAP)

lint-strict:
	@$(PYTHON_PATH) -m flake8 $(FILES)
	@$(PYTHON_PATH) -m $(MYPY) $(FILES) --strict

