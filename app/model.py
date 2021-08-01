from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class user(db.Model):
    __tablename__ = 'list'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    writter = db.Column(db.String(11), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(10), nullable=False)


def __init__(self, id, writter, description, created, password):
    self.id = id
    self.writter = writter
    self.description = description
    self.created = datetime.now()
    self.password = password
