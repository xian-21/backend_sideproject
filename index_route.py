from flask import Blueprint, render_template
from flask_login import login_required, current_user



index_routes = Blueprint('index_routes', __name__)

@index_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

# 其他首頁相關的路由和功能移至此
