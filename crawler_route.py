from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from pymongo.mongo_client import MongoClient

crawler_routes = Blueprint('crawler_routes', __name__)

# 資料庫連線
client = MongoClient("mongodb+srv://a8979401551:q6S9BNqbUgwZTvmJ@cluster0.zeyfhie.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.crawler
user_collection = db['user']

# 其他爬蟲相關的路由和功能移至此

@crawler_routes.route("/crawler", methods=['GET', 'POST'])
@login_required
def crawler():
    if request.method == 'POST':
        print('post進入')
        pair = request.form.get("crypto_pairs")
        price = request.form.get("noti_price")
        email = request.form.get("email")
        l_p = request.form.get('upper_lower')
        search_email = request.form.get('search_noti')

        print(pair,'交易對')
        db = client.crawler
        user_collection = db['user']
        
        if search_email:
            crawler_user = user_collection.find({'email': search_email}) #搜尋特定email
            user_list = list(crawler_user)
            if user_list != []:
                return render_template('crawler.html', data= user_list)
            else:
                return render_template('crawler.html', data= '此信箱沒有提醒紀錄')
        else:
            print('信箱為空值')
        

        insert_noti = user_collection.find({'email': email})
        lsit_insert_noti = list(insert_noti)
        if lsit_insert_noti == []:#搜尋資料庫 如果email不存在資料庫就寫入
            user_collection.insert_one(
                {
                    'email': email,
                    'pair': pair,
                    'price': price,
                    'upper_lower': l_p
                }
            )
            print(str(email) + '新增提醒')
            flash(str(email) + '新增提醒')
        elif lsit_insert_noti: #確定信箱已經新增過
            insert_noti = user_collection.find({'email': email})
            total_pair = []
            for i in insert_noti:
                total_pair.append(i['pair'])
            if pair not in total_pair: #確定信箱沒有設過該交易對的提醒
                user_collection.insert_one(
                    {
                        'email': email,
                        'pair': pair,
                        'price': price,
                        'upper_lower': l_p
                    }
                )
                print(email + '還沒有' + pair + '的提醒  新增提醒')
                flash(email + '還沒有' + pair + '的提醒  新增提醒')
            else:
                flash('此交易對已經設過提醒')
                print('此交易對已經設過提醒')
            
        else:
            print('此組合已存在')
            flash('此組合已存在')
    else:
        print('get進入crawler........')
        return render_template('crawler.html')
 
    return render_template('crawler.html')
