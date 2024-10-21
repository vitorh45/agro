clean:
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -delete
	find . -name .pytest_cache | xargs rm -rf
	rm -f .coverage
	rm -rf htmlcov

test: clean
	pytest src/tests/ -s -v

coverage: clean
	pytest -s -v --rootdir=src/tests --cov=src/api --cov-branch --cov-report=term --cov-report=html src/tests/
