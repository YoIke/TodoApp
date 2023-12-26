from flask import Blueprint, request, jsonify, current_app, make_response
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
            'username': user.username,  # ユーザーネームをトークンに追加
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        # トークンをHTTP Onlyクッキーにセット
        response = make_response(jsonify({'message': 'Logged in successfully'}), 200)
        response.set_cookie('token', token, httponly=True, samesite='Lax')
        
        # ユーザーネームを別のクッキーとしてセット
        response.set_cookie('username', user.username, httponly=True, samesite='Lax')

        return response
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get('token')

    # トークンが存在しない、または無効な場合
    if not token:
        return jsonify({'error': 'Not logged in'}), 401

    try:
        # トークンの検証
        jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return jsonify({'error': 'Invalid token'}), 401

    # トークンが有効な場合、ログアウト処理を実行
    response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
    response.set_cookie('token', '', expires=0)  # トークンを削除
    return response

    
@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    token = request.cookies.get('token')
    if token:
        try:
            # トークンの検証
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            # ユーザーネームのクッキーを取得
            username = request.cookies.get('username', 'Unknown')  # デフォルト値を設定

            return jsonify({
                'isAuthenticated': True,
                'username': username
            }), 200
        except:
            return jsonify({'isAuthenticated': False}), 401
    else:
        return jsonify({'isAuthenticated': False}), 401


    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # HTTPヘッダーではなくクッキーからトークンを取得
        token = request.cookies.get('token')

        if not token:
            current_app.logger.error('Token is missing in the request cookie')
            return jsonify({'message': 'Token is missing!'}), 403

        current_app.logger.debug(f'Received token from cookie: {token}')

        try:
            # トークンをデコードし、ユーザーIDを取得
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            current_app.logger.debug(f'Decoded data: {data}')
        except Exception as e:
            current_app.logger.error(f'Token decoding error: {str(e)}')
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated_function

