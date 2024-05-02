from flask import Blueprint, flash, redirect
from flask_login import login_required, logout_user
from flask import session

logout_route = Blueprint('logout', __name__)


@logout_route.route("/logout", methods=['GET', 'POST'])
@login_required  # 這個裝飾器確保只有已登入的用戶才能訪問這個路由
def logout():
    session.clear()
    logout_user()
    flash('You have been logged out successfully.')
    return redirect('/')