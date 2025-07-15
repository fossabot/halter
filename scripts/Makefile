.PHONY: venv install lint test build publish clean

venv:
	uv venv

install: venv
	uv sync

lint:
	uv run ruff check src

test:
	uv run pytest --cov=src --junitxml=junit.xml

build:
	sed -n '1,/
/p' pyproject.toml && python -m build --wheel --sdist

publish:
	twine upload dist/*

clean:
	rm -rf dist build *.egg-info junit.xml __pycache__
