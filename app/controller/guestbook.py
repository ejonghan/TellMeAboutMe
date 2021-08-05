from flask import render_template, Blueprint, request, redirect, url_for
from app.model import model

blueprint = Blueprint("guestbook", __name__, url_prefix="/")

@blueprint.route("/guestbook_list", methods=['GET'])
def guestbook_list():

    if request.method == 'GET':
        # database select query
        select_user = model.user.query.all()
        users = {}
        # create dict using script
        for i in range(len(select_user)):

            users[str(select_user[i].id)] = f"{select_user[i].writter}님의 게시물"

        return render_template('/guestbook_list.html', users=users)

@blueprint.route('/guestbook', methods=['GET'])
def guestbook():

    if request.method == 'GET':

        get_id = request.args.get('id')
        select_user = model.user.query.filter_by(id=get_id).all()
        select_user = select_user[0]

        return render_template('/guestbook.html', select_user = select_user, get_id=get_id)


@blueprint.route('/guestbook/<int:id>', methods=['GET'])
def anchor_routing_guestbook(id):

    return redirect(url_for('guestbook.guestbook', id=id))