
c:
	echo -n "" > db.csv

jsons:
	bash db2jsons.sh

doctest:
	venv/bin/python -m pytest --doctest-modules ./conv

t:
	venv/bin/python test.py




