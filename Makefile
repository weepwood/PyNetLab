SHELL := /bin/bash
PYTHON ?= .venv/bin/python

.PHONY: help setup test lint c c-optional clean

help:
	@printf '%s\n' \
	  'make setup       Create Python environment and install dependencies' \
	  'make test        Run Python unit and integration tests' \
	  'make lint        Run Ruff' \
	  'make c           Compile C labs that need only libc/Linux headers' \
	  'make c-optional  Compile optional liburing lab' \
	  'make clean       Remove generated artifacts'

setup:
	./scripts/setup_ubuntu.sh

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(PYTHON) -m ruff check src tests

c:
	$(MAKE) -C c all

c-optional:
	$(MAKE) -C c optional

clean:
	$(MAKE) -C c clean
	rm -rf .ruff_cache .mypy_cache build dist *.egg-info src/*.egg-info
