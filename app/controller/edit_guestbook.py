from flask import Blueprint, json, request, render_template
from app.model import model

blueprint = Blueprint("edit_guestbook", __name__, url_prefix="/")

@blueprint.route('/delete', methods=["DELETE"])
def delete():

    info = request.get_json()

    get_id = info['id']
    origin_password = info['origin_password']
    input_password = info['input_password']

    if origin_password == input_password:

        # database delete query
        select_user = model.user.query.filter_by(id = get_id).all()
        select_user = select_user[0]
        model.db.session.delete(select_user)
        model.db.session.commit()
        model.db.session.remove()
        
        return json.dumps("yes")

    else:
        return json.dumps("no")


@blueprint.route('/update', methods=["PUT"])
def update():

    info = request.get_json()

    get_id = info['id']
    get_writter = info['writter']
    get_description = info['description']

    if get_writter == "":
        return json.dumps("empty_writter")
    elif get_description == "":
        return json.dumps("empty_description")
    else:

        user = model.user.query.get(get_id)
        user.writter = get_writter
        user.description = get_description
        model.db.session.commit()
        model.db.session.remove()

        return json.dumps("yes")


@blueprint.route('/update_passwordcheck', methods=["POST"])
def update_passwordcheck():

    info = request.get_json()

    origin_password = info['origin_password']
    input_password = info['input_password']

    if origin_password == input_password:

        return json.dumps("yes")

    else:
        return json.dumps("no")


@blueprint.route('/update_form/<string:get_id>', methods=["GET"])
def update_form(get_id):

    return render_template("/update_form.html", get_id=get_id)


@blueprint.route('/password_check', methods=["POST"])
def password_check():

    _method = request.form['_method']
    get_id = request.form['id']
    password = request.form['password']

    return render_template('checkpassword.html', _method=_method, get_id=get_id, password=password)
