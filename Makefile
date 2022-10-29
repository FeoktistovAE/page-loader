install:
	poetry install
build: check
	poetry build
package-install:
	python3 -m pip install dist/*.whl
lint:
	poetry run flake8 page_loader tests
test:
	poetry run pytest
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml
selfcheck:
	poetry check
check: selfcheck
setup: install build package-install