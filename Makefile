i:
	pip install ${i} && pip freeze > requirements.txt

ia:
	pip install -r requirements.txt