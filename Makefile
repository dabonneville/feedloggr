
PACKAGE_NAME=feedloggr

analyze:
	. env/bin/activate && \
	pylint tests.py example/*.py feedloggr/*.py | less

test:
	. env/bin/activate && \
	coverage run --source=feedloggr tests.py
	rm -f test.db

clean:
	rm -f $(PACKAGE_NAME)/*.pyc
	rm -f example/*.pyc
	rm -f *.pyc
