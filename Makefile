test:
	coverage run --omit=venv manage.py test
	coverage html