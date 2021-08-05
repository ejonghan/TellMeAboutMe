FROM python:3.7

RUN pip3 install flask pymysql datetime flask_sqlalchemy

COPY . .

CMD python3 run.py 

