.PHONY: test lint format typecheck install

install:
	uv pip install -e .[dev]

test:
	pytest tests/

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/
