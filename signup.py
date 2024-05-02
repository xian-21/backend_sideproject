from flask import Blueprint, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from werkzeug.security import generate_password_hash


signup_route = Blueprint('signup_route', __name__)


@signup_route.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')



@signup_route.route('/signup_req', methods=['POST'])
def signup_req():
    data = request.json
    print('Received data', data)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    hashed_password = generate_password_hash(password)

    client = MongoClient("mongodb+srv://a8979401551:q6S9BNqbUgwZTvmJ@cluster0.zeyfhie.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.signup
    collection = db['user_data']

    existing_user = collection.find_one({'email': email})
    print(existing_user,'asdas')
    if existing_user != None:
        return jsonify({'error': 'Email already registered'}), 400
    else:
        try:
            print('註冊')
            collection.insert_one({'email': email, 'password': hashed_password})
            print('132123')
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500