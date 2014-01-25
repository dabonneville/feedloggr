
PACKAGE_NAME=feedloggr

analyze:
	pylint tests.py example/*.py $(PACKAGE_NAME)/*.py | less

test:
	coverage run --source=$(PACKAGE_NAME) tests.py
	rm -f test.db

clean:
	rm -f $(PACKAGE_NAME)/*.pyc
	rm -f example/*.pyc
	rm -f *.pyc
