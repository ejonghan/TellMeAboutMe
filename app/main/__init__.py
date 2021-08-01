from app.main.index import main as main
from flask import Flask
from app.module.dbModule import Database

app = Flask(__name__)
db = Database()

app.register_blueprint(main)
