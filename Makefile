default: up

i:
	pip3 install ${i} && pip3 freeze | grep ${i}== | sed 's/$$/ /g' >> requirements.txt

ia:
	pip3 install -r requirements.txt

up:
	docker-compose up

build:
	docker-compose up --build --no-deps server

build-db:
	docker-compose up --build db

build-all:
	docker-compose build --no-cache

shell:
	docker exec -it ppp_server bash

test:
	pytest tests/
