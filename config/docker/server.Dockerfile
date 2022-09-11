FROM python:3.10
ADD . /www/
WORKDIR /www

RUN apt-get update
RUN apt-get install python3-pymysql -y
RUN pip3.10 install -r requirements.txt

CMD python3 main.py