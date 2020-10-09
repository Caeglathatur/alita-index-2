format:
	black .

check:
	coverage run -m pytest --black
	coverage report
	flake8
