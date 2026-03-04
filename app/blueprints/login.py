from flask import Blueprint, jsonify, request, session
import bcrypt
import mysql.connector  # 确保导入mysql.connector
from . import tool
import jwt
import time
from functools import wraps

# 创建蓝图
login = Blueprint('login', __name__, url_prefix='/login')

SECRET_KEY = "your_secure_secret_key_never_share_it"
@login.route('/user', methods=['POST'])
def user_login():
    # 获取JSON数据
    data = request.get_json()
    print(data)

    card = data['username']
    password = data['password']


    # 获取数据库连接
    connection = tool.get_db_connection('health_record')
    cursor = connection.cursor(dictionary=True)

    # 查询用户
    query = "SELECT password_hash FROM record WHERE card = %s"
    cursor.execute(query, (card,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            'success': False,
            'message': '用户名不存在'
        })

    # 验证密码
    stored_hash = user['password_hash'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        # 在session中记录登录状态
        session['username'] = card
        session['is_authenticated'] = True
        payload = {
            "user_id": card,  # 用户唯一标识（从数据库获取）
            "username": card,
            "exp": int(time.time()) + 3600 * 24 * 7  # 过期时间：7天（按需调整）
        }
        # 用密钥签名生成 Token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # 4. 返回 Token 给前端（前端存储 Token，后续请求携带）
        return jsonify({
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "user_info": {"user_id": card, "username": card}  # 可选：返回用户基本信息
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '密码错误'
        })

@login.route('/volunteer', methods=['POST'])
def volunteer_login():
    # 获取JSON数据
    data = request.get_json()
    print(data)

    card = data['username']
    password = data['password']



    connection = tool.get_db_connection('users-information')
    cursor = connection.cursor(dictionary=True)


    query = "SELECT password_hash FROM volunteer WHERE card = %s"
    cursor.execute(query, (card,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            'success': False,
            'message': '用户名不存在'
        })

    # 验证密码
    stored_hash = user['password_hash'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        # 在session中记录登录状态
        session['username'] = card
        session['is_authenticated'] = True
        payload = {
            "user_id": card,  # 用户唯一标识（从数据库获取）
            "username": card,
            "exp": int(time.time()) + 3600 * 24 * 7  # 过期时间：7天（按需调整）
        }
        # 用密钥签名生成 Token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # 4. 返回 Token 给前端（前端存储 Token，后续请求携带）
        return jsonify({
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "user_info": {"user_id": card, "username": card}  # 可选：返回用户基本信息
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '密码错误'
        })





@login.route('/admin', methods=['POST'])
def admin_login():
    # 获取JSON数据
    data = request.get_json()
    print(data)

    card = data['username']
    password = data['password']


    # 获取数据库连接
    connection = tool.get_db_connection('users-information')
    cursor = connection.cursor(dictionary=True)

    # 查询用户
    query = "SELECT password_hash FROM users WHERE card = %s"
    cursor.execute(query, (card,))
    user = cursor.fetchone()

    if not user:
        return jsonify({
            'success': False,
            'message': '用户名不存在'
        })

    # 验证密码
    stored_hash = user['password_hash'].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        # 在session中记录登录状态
        session['username'] = card
        session['is_authenticated'] = True
        payload = {
            "user_id": card,  # 用户唯一标识（从数据库获取）
            "username": card,
            "exp": int(time.time()) + 3600 * 24 * 7  # 过期时间：7天（按需调整）
        }
        # 用密钥签名生成 Token
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        # 4. 返回 Token 给前端（前端存储 Token，后续请求携带）
        return jsonify({
            "code": 200,
            "message": "登录成功",
            "data": {
                "token": token,
                "user_info": {"user_id": card, "username": card}  # 可选：返回用户基本信息
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': '密码错误'
        })





@login.route('/status', methods=['GET'])
def login_status():
    if 'username' in session and session['is_authenticated']:
        return jsonify({
            'isLoggedIn': True,
            'username': session['username']
        })
    else:
        return jsonify({
            'isLoggedIn': False
        })


# 登出接口
@login.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': '已成功登出'
    })
