from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'your_secret_key'

users = {}  # In-memory user storage for simplicity

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    avatar = data.get('avatar', 'default_avatar.png')
    if username in users:
        return jsonify({'message': 'User already exists!'}), 400
    users[username] = {'password': password, 'avatar': avatar}
    return jsonify({'message': 'User registered successfully!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401
    token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY)
    return jsonify({'token': token, 'avatar': user['avatar']})

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorator
