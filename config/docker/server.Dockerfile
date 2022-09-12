FROM python:3.10 as build
ADD . /www/
WORKDIR /www

RUN apt-get update
RUN apt-get install python3-pymysql -y
RUN pip3.10 install -r requirements.txt

from build as test
CMD pytest src/tests/ --cov=src -vv

from build as dev
CMD python3 main.py