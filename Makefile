.PHONY: install dev test lint format db clean run

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install || true

db:
	sqlite3 nexus.db < db/schema.sql
	@echo "DB initialized: nexus.db"

test:
	pytest -v

lint:
	ruff check nexus/ tests/
	mypy nexus/ || true

format:
	ruff format nexus/ tests/

run:
	nexus run --task "Hello NEXUS"

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache __pycache__
	find . -name "__pycache__" -type d -exec rm -rf {} +
