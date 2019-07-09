#requires the installation of packages python, python-dev, postgresql-server-dev-9.5
#and the installation and instanciation of a python virtualenv called venv in the api directory

. venv/bin/activate

pip install flask
pip install flask_restful
pip install psycopg2
pip install ConfigParser
pip install StringGenerator
pip install pyjwt
