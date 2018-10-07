from flask import Blueprint, render_template
from poptraq import app

admin = Blueprint('admin', __name__, url_prefix='/admin', static_folder='static', template_folder='templates')


@admin.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(admin)
