.PHONY: install dev test lint format clean build publish help

help:
	@echo "Git Quick - Development Commands"
	@echo ""
	@echo "install     Install package"
	@echo "dev         Install in development mode"
	@echo "test        Run tests"
	@echo "lint        Run linters"
	@echo "format      Format code"
	@echo "clean       Clean build artifacts"
	@echo "build       Build package"
	@echo "publish     Publish to PyPI"

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	pytest --cov=git_quick tests/ -v

lint:
	ruff check git_quick tests
	mypy git_quick

format:
	black git_quick tests
	ruff check --fix git_quick tests

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

# VS Code extension
vscode-install:
	cd vscode-extension && npm install

vscode-build:
	cd vscode-extension && npm run compile

vscode-package:
	cd vscode-extension && npx vsce package

vscode-publish:
	cd vscode-extension && npx vsce publish
