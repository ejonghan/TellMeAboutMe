from .controller import index, submit, guestbook, edit_guestbook
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1005@localhost:3306/tellmeaboutme"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "hungryjohns"

db = SQLAlchemy(app)

app.register_blueprint(index.main)
app.register_blueprint(submit.blueprint)
app.register_blueprint(guestbook.blueprint)
app.register_blueprint(edit_guestbook.blueprint)