from flask import Blueprint, request, render_template, flash, redirect
from flask_login import login_user, current_user, LoginManager, UserMixin
from pymongo.mongo_client import MongoClient
from werkzeug.security import check_password_hash



# 資料庫連線
client = MongoClient("mongodb+srv://a8979401551:q6S9BNqbUgwZTvmJ@cluster0.zeyfhie.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.signup
user_collection = db['user_data']
cursor = user_collection.find({}, {'_id': 0, 'email': 1, 'password': 1})




login_routes = Blueprint('login_routes', __name__)



login_manager = LoginManager()
login_manager.login_view = "/"  # 设置登录视图，使用根路径作为登录页面
login_manager.login_message = "請先登入！"  # 可选，自定义未登录提示消息


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_id(self):
        return str(self.id)





@login_manager.user_loader
def user_loader(user_id):
    print('使用user_loader')
    user_data = user_collection.find_one({'email': user_id})
    if user_data:
        user = User(user_id)
        user.id = user_id
        print('user_load',user.id)
        return user
    return None

@login_manager.request_loader
def request_loader(request):
    print('使用request_loader')
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    user_data = user_collection.find_one({'email': user_id}) 
    if user_data and check_password_hash(user_data['password'], password):
        user = User(user_id)
        user.id = user_id
        
        return user
    return None




# 其他功能和路由移至此

@login_routes.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user_data = user_collection.find_one({'email': user_id})
        
        if user_data and check_password_hash(user_data['password'], password):

            
            user = User(user_id)
            user.id = user_id
            
            login_user(user) # 使用剛剛創建的用戶對象來登錄
            print(user.is_authenticated,'user.is_authenticated')
            print("User logged in successfully:", current_user.get_id())
            print(current_user.is_authenticated,'current_user.is_authenticated')
            flash('Logged in successfully.')
            return redirect('/index')

        else:
            flash('Invalid username or password.')
            return redirect('/')  # Unauthorized
    return render_template('login.html', current_user=current_user)
