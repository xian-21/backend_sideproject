from flask import Blueprint, request, jsonify, current_app
from pymongo.mongo_client import MongoClient
from pymongo import UpdateOne
import os

update_route = Blueprint('update_route', __name__)

#蒐集好所有待更新的資料(bulk_update type=list ) 一次更新到資料庫裡
def update_database(bulk_update):
    # 資料庫連線
    client_ = os.environ.get('DATABASE_URL')
    client = MongoClient(client_)
    client = MongoClient("mongodb+srv://a8979401551:kVUJDErEzB1Bl6lg@cluster0.zeyfhie.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.crawler
    collection = db['user']
    try:
        result = collection.bulk_write(bulk_update)
    except:
        print('出錯')
    return result



@update_route.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

#修改提醒資料
@update_route.route('/update-alert-all', methods=['POST'])
def update_alert():
    if request.headers['Content-Type'] == 'application/json':
        try:
            data = request.get_json() 
            bulk_update = []
            for data_ in data:
                email = data_['email']
                pair = data_['pair']
                upper_lower = data_['upper_lower']
                price = data_['price']
                bulk_update.append(UpdateOne(
                    {"email": email, 'pair': pair},  # 查詢條件
                    {"$set": {'upper_lower': upper_lower, 'price': price}}      # 更新操作
                ))
            print(bulk_update)
            result = update_database(bulk_update)
            
            if result and result.bulk_api_result['nModified'] > 0:
                print('成功修改資料')
                
                return jsonify({'message': 'Alert updated successfully'}), 200
            else:
                print('沒有修改資料')
                return jsonify({'message': 'No changes were made'}), 200

        except Exception as e:
            current_app.logger.error(f"Error processing request: {e}")
            return jsonify({'error': 'Error processing request'}), 400
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415
