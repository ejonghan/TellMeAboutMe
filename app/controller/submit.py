from flask import render_template, Blueprint

blueprint = Blueprint('submit', __name__ , url_prefix='/')

@blueprint.route('/submit', methods=['GET'])
def submit():

    return render_template('/submit.html')