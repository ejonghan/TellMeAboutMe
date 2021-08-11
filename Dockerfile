FROM python:3.7

RUN pip3 install flask pymysql flask_sqlalchemy

COPY . .

CMD python3 run.py 

