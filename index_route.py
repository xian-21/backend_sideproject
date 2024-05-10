from flask import Blueprint, render_template
from flask_login import login_required



index_routes = Blueprint('index_routes', __name__)

@index_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


