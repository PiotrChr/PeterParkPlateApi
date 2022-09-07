FROM python:3.10.7
ADD . /www/
WORKDIR /www
RUN pip install -r requirements.txt
CMD python3 main.py