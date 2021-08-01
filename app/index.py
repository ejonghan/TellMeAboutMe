from flask import Blueprint, request, render_template, redirect, url_for, json
from flask import current_app as app
from app.module.dbModule import Database
from app import model
from datetime import datetime

main = Blueprint('main', __name__, url_prefix='/')
db = Database()


@main.route('/', methods=['GET'])
def main_page():
    
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


@main.route('/submit', methods=['GET'])
def submit():

    return render_template('/submit.html')


@main.route('/guestbook_list', methods=['GET'])
def guestbook_list():

    if request.method == 'GET':

        # database select query
        sql = "SELECT * FROM tellmeaboutme.list"
        view = db.executeAll(sql)

        view_dict = {}

        # create dict using script
        for i in range(len(view)):

            view_dict[str(view[i]['id'])] = f"{view[i]['writter']}님의 게시물"

        return render_template('/guestbook_list.html', view_dict=view_dict)


@main.route('/guestbook', methods=['GET'])
def guestbook():

    if request.method == 'GET':

        get_id = request.args.get('id')

        sql = f"SELECT * FROM tellmeaboutme.list WHERE id={get_id}"
        view = db.executeOne(sql)

        return render_template('/guestbook.html', view=view, get_id=get_id)


@main.route('/guestbook/<int:id>', methods=['GET'])
def anchor_routing_guestbook(id):

    return redirect(url_for('main.guestbook', id=id))


@main.route('/delete', methods=["DELETE"])
def delete():

    info = request.get_json()

    get_id = info['id']
    origin_password = info['origin_password']
    input_password = info['input_password']

    if origin_password == input_password:

        # database delete query
        delete_sql = f"DELETE FROM tellmeaboutme.list WHERE id={get_id}"
        db.execute(delete_sql)

        # database auto_increment(id value) rearrange query
        auto_increment_sql1 = "ALTER TABLE tellmeaboutme.list AUTO_INCREMENT=1"
        db.execute(auto_increment_sql1)
        auto_increment_sql2 = "SET @count = 0"
        db.execute(auto_increment_sql2)
        auto_increment_sql3 = "UPDATE tellmeaboutme.list SET id = @count:=@count+1"
        db.execute(auto_increment_sql3)
        db.commit()

        return json.dumps("yes")

    else:
        return json.dumps("no")


@main.route('/update', methods=["PUT"])
def update():

    info = request.get_json()

    get_id = info['id']
    writter = info['writter']
    description = info['description']

    if writter == "":
        return json.dumps("empty_writter")
    elif description == "":
        return json.dumps("empty_description")
    else:

        update_sql1 = "UPDATE tellmeaboutme.list SET writter='%s' WHERE id='%s'" % (
            writter, get_id)
        db.execute(update_sql1)
        update_sql2 = "UPDATE tellmeaboutme.list SET description='%s' WHERE id='%s'" % (
            description, get_id)
        db.execute(update_sql2)
        db.commit()

        return json.dumps("yes")


@main.route('/update_passwordcheck', methods=["POST"])
def update_passwordcheck():

    info = request.get_json()

    origin_password = info['origin_password']
    input_password = info['input_password']

    if origin_password == input_password:

        return json.dumps("yes")

    else:
        return json.dumps("no")


@main.route('/update_form/<string:get_id>', methods=["GET"])
def update_form(get_id):

    return render_template("/update_form.html", get_id=get_id)


@main.route('/password_check', methods=["POST"])
def password_check():

    _method = request.form['_method']
    get_id = request.form['id']
    password = request.form['password']

    return render_template('checkpassword.html', _method=_method, get_id=get_id, password=password)
