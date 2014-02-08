
PACKAGE_NAME=feedloggr

analyze:
	pylint tests.py example/*.py $(PACKAGE_NAME)/*.py | less

test:
	coverage run --source=$(PACKAGE_NAME) tests.py
	rm -f test.db

sdist:
	python setup.py sdist

clean:
	rm -fr dist/
	rm -fr $(PACKAGE_NAME).egg-info/
	rm -f $(PACKAGE_NAME)/*.pyc
	rm -f example/*.pyc
	rm -f *.pyc

