ACTIVATE_ENVIRONMENT=pipenv shell
RUN_ENV=pipenv run

install_environment:
	pip install pipenv;\
	pipenv install

run_tests:
	$(RUN_ENV) python -m pytest *.py

fix_code_formatting:
	$(RUN_ENV) yapf -i --style=setup.cfg *.py
