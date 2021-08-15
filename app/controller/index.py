from flask import Blueprint, request, render_template, redirect, url_for, json
from app.model import model
from datetime import datetime
from sqlalchemy import text

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=['GET'])
def main_page():
    print(1)
    return render_template('/main/index.html')


@main.route('/input_form', methods=['POST'])
def input_form():
    if request.method == 'POST':

        # form data preprocesscing
        form_data = request.get_json()

        input_writter = form_data['writter']
        input_description = form_data['description']
        input_password = form_data['password']

        if input_writter == "":
            return json.dumps("empty writter")

        elif input_description == "":
            return json.dumps("empty description")

        elif input_password == "":
            return json.dumps("empty password")

        else:
            # database insert query
            data = model.user(
                writter = input_writter,
                description = input_description,
                created = datetime.now(),
                password = input_password
            )

            model.db.session.add(data)
            model.db.session.commit()
            model.db.session.remove()

            return json.dumps("yes")

@main.route('/add_data', methods=["POST"])
def add_data():
    if request.method == 'POST':

        get_data = request.get_json()

        for i in range(100):
            
            data = model.user(
                writter = str(i),
                description = str(i),
                created = datetime.now(),
                password = str(123)
            )

            model.db.session.add(data)
            model.db.session.commit()
            model.db.session.remove()
        
        return json.dumps("yes")