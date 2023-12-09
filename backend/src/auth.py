from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import jwt
import datetime
from functools import wraps


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email and password are required'}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')  # ユーザーネームの代わりにメールアドレスを使用
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()  # メールアドレスでユーザーを検索
    if user and check_password_hash(user.password_hash, password):
        # トークンの生成
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # 有効期限の設定
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token, 'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            current_app.logger.error('Token is missing in the request header')
            return jsonify({'message': 'Token is missing!'}), 403

        token = token.split(" ")[1] if ' ' in token else token  # Bearer トークンの処理
        current_app.logger.debug(f'Received token: {token}')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            current_app.logger.debug(f'Decoded data: {data}')
        except Exception as e:
            current_app.logger.error(f'Token decoding error: {str(e)}')
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated_function
