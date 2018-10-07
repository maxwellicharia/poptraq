from flask import Blueprint, render_template
from poptraq import app

errors = Blueprint('errors', __name__, url_prefix='/errors', static_folder='static', template_folder='templates')


@errors.route('/general')
def general():
    return render_template('401.html')


app.register_blueprint(errors)
