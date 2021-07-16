from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify, json
from flask import current_app as app

from app.module.dbModule import Database

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')


@main.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        # form data preprocesscing
        writter = request.form['writter']
        description = request.form['description']
        password = request.form['password']

        # database insert query
        db = Database()
        sql = "INSERT INTO tellmeaboutme.list(writter, description, created, password) VALUES('%s', '%s', NOW(), '%s')" % (
            writter, description, password)
        db.execute(sql)
        db.commit()

        return render_template('/submit.html')


@main.route('/guestbook_list', methods=['GET', 'post', 'DELETE'])
def guestbook_list():
    if request.method == 'GET':

        # database select query
        db = Database()
        sql = "SELECT * FROM tellmeaboutme.list"
        view = db.executeAll(sql)

        view_dict = {}

        # create dict using script
        for i in range(len(view)):

            view_dict[str(view[i]['id'])] = f"{view[i]['writter']}님의 게시물"

        return render_template('/guestbook_list.html', view_dict=view_dict)

    elif request.method == 'POST':

        # database select query
        db = Database()
        sql = "SELECT * FROM tellmeaboutme.list"
        view = db.executeAll(sql)

        view_dict = {}

        # create dict using script
        for i in range(len(view)):

            view_dict[str(view[i]['id'])] = f"{view[i]['writter']}님의 게시물"

        return render_template('/guestbook_list.html', view_dict=view_dict)

    elif request.method == 'DELETE':

        # database select query
        db = Database()
        sql = "SELECT * FROM tellmeaboutme.list"
        view = db.executeAll(sql)

        view_dict = {}

        # create dict using script
        for i in range(len(view)):

            view_dict[str(view[i]['id'])] = f"{view[i]['writter']}님의 게시물"
        print(view_dict)
        return render_template('/guestbook_list.html', view_dict=view_dict)


@main.route('/guestbook', methods=['GET', 'POST'])
def guestbook():

    # routed when you click '보기' button
    if request.method == 'POST':

        get_id = request.form['id']

        db = Database()
        sql = f"SELECT * FROM tellmeaboutme.list WHERE id={get_id}"
        view = db.executeOne(sql)

        return render_template('/guestbook.html', view=view, get_id=get_id)

    # routed when you clink anchor tag
    else:

        get_id = request.args.get('id')

        db = Database()
        sql = f"SELECT * FROM tellmeaboutme.list WHERE id={get_id}"
        view = db.executeOne(sql)

        return render_template('/guestbook.html', view=view, get_id=get_id)


@main.route('/guestbook/<int:id>', methods=['GET'])
def anchor_routing_guestbook(id):

    return redirect(url_for('main.guestbook', _method='POST', id=id))


@main.route('/delete', methods=["DELETE"])
def delete():

    info = request.get_json()

    get_id = info['id']
    origin_password = info['origin_password']
    input_password = info['input_password']
    print(info)

    if origin_password == input_password:
        db = Database()

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

        print(url_for('main.guestbook_list'))
        return json.dumps("yes")

    else:
        return json.dumps("no")


@main.route('/update', methods=["UPDATE"])
def update():

    info = request.get_json()

    get_id = info['id']
    writter = info['writter']
    description = info['description']

    db = Database()

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
    print(info)
    origin_password = info['origin_password']
    input_password = info['input_password']

    if origin_password == input_password:

        return json.dumps("yes")

    else:
        return json.dumps("no")


@main.route('/update_form/<string:get_id>', methods=["GET"])
def update_form(get_id):

    return render_template("/update_form.html", get_id=get_id)


@main.route('/divide_method', methods=["POST"])
def divide_method():

    _method = request.form['_method']
    get_id = request.form['id']
    password = request.form['password']
    print(_method)

    return render_template('checkpassword1.html', _method=_method, get_id=get_id, password=password)
