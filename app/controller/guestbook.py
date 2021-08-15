from flask import render_template, Blueprint, request, redirect, url_for
from flask_sqlalchemy import Pagination
from app.model import model

blueprint = Blueprint("guestbook", __name__, url_prefix="/")

@blueprint.route("/guestbook_list/", methods=['GET'])
def guestbook_list():

    if request.method == 'GET':

        # GET 방식으로 요청한 url을 page값으로 가져오기위해 
        page = request.args.get('page', type=int, default=1)

        # database select query
        select_user = model.user.query.all()

        # pagenation 객체 생성
        page_data = model.user.query.paginate(page, 10 , error_out=False)

        # Queue pool overflow error 방지를 위해 
        # 매번 query를 날릴때마다 작업 후 seesion을 끊어준다
        model.db.session.remove()

        return render_template('/guestbook_list.html', page_data=page_data)

@blueprint.route('/guestbook', methods=['GET'])
def guestbook():

    if request.method == 'GET':

        get_id = request.args.get('id')
        select_user = model.user.query.filter_by(id=get_id).all()
        model.db.session.remove()
        select_user = select_user[0]

        return render_template('/guestbook.html', select_user = select_user, get_id=get_id)


@blueprint.route('/guestbook/<int:id>', methods=['GET'])
def anchor_routing_guestbook(id):

    return redirect(url_for('guestbook.guestbook', id=id))