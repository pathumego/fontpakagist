
install: venv-install fib-install

venv-install:
	virtualenv .env --distribute --prompt=\(fib\)

fib-install:
	. .env/bin/activate; pip install -r requirements.txt; python setup.py install
	# enable access to system site-packages for python-fontforge
	rm .env/lib/python2.7/no-global-site-packages.txt

