from flask import Flask
from login_route import login_routes
from index_route import index_routes
from crawler_route import crawler_routes
from logout import logout_route
from flask_login import LoginManager
from login_route import login_manager  # 假設您的 auth.py 和 main.py 在同一個目錄下
from update_alert import update_route
from signup import signup_route

app = Flask(__name__)
app.secret_key = '0521'
login_manager.init_app(app)


app.register_blueprint(signup_route)
app.register_blueprint(update_route)
app.register_blueprint(login_routes)
app.register_blueprint(index_routes)
app.register_blueprint(crawler_routes)
app.register_blueprint(logout_route)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
