import os 
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint
import schedule
import time
import requests
# 蒐集資料庫裡每個信箱設的提醒價格 > 蒐集交易對價格 > 比對交易對價格跟每個信箱的提醒價格有無觸發
 

crawler_routes = Blueprint('binance_api', __name__)

def get_symbol_price():
    url = 'https://api.binance.com/api/v3/ticker/price'
    symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT', 'BNBUSDT', '1000SATSUSDT', 'SAGAUSDT', 'OMNIUSDT', 'SOLUSDT', 'PEPEUSDT', 'DOGEUSDT']
    price = {}
    response = requests.get(url)
    data = response.json()
    for item in data:
        if item['symbol']  in symbols:
            price[item['symbol']] = item['price'].rstrip('0')
    return price


def send_email(email, pair, price):
    sender_email = "nov2531456@gmail.com"
    receiver_email = email
    subject = f"{pair} 價格超過閾值提醒"
    body = f"交易對 {pair} 當前價格為 {price} 已經達到您設置的價格"
    
    # 創建郵件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # 連接到 SMTP 服務器並發送郵件
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, "wxqv jcbh hmqv blvr")
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)


def notify():
    # 資料庫連線
    database_client = os.environ.get('DATABASE_URL')
    database_client = MongoClient("mongodb+srv://a8979401551:kVUJDErEzB1Bl6lg@cluster0.zeyfhie.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = database_client.crawler
    user_collection = db['user']
    # 擷取集合中的所有資料
    all_data = user_collection.find()
    pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT', 'BNBUSDT', 'OMNIUSDT', 'SOLUSDT', 
            'DOGEUSDT']
    all_data = list(all_data)
    no_noti_pair = []
    noti_pair = []
    for pair in pairs:
        datas = []
        for data in all_data:
            if data['pair'] == pair:
                datas.append(data)
        emails = ''
        #datas 取得同交易對的所有價格設置價位
        price = get_symbol_price()
        for data in datas:
            #當市場價大於設定價格就寄信給該email
            if data['upper_lower'] == 'upper' and float(price[pair]) > float(data['price']):
                emails = emails + data['email'] + ','
                user_collection.delete_one({'_id': data['_id']})
                print('刪除')
            #當市場價低於設定價格就寄信給該email
            elif data['upper_lower'] == 'lower' and float(price[pair]) < float(data['price']):
                emails = emails + data['email'] + ','
                user_collection.delete_one({'_id': data['_id']})
                print('刪除')
        if emails != '':
            send_email(emails, pair, price)
            noti_pair.append(pair)
            print('信件寄出 :　',emails)
        elif emails == '':
            no_noti_pair.append(pair)
    print('信件寄出 :　',noti_pair)
    print('未發現提醒', no_noti_pair)


def schedule_task():
    schedule.every(1).minutes.do(notify)
    # 開始執行定時任務
    while True:
        schedule.run_pending()
        time.sleep(1)

