FROM python:3.7

RUN pip3 install flask pymysql pytest

COPY . .

CMD python3 run.py 

