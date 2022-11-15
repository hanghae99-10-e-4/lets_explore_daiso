from flask import Blueprint, jsonify, request, make_response
import hashlib
from db_connect import mongodb
import datetime
import jwt
from dotenv import load_dotenv
from pathlib import Path
import os

join_api = Blueprint('join_api', __name__)
id_check_api = Blueprint('id_check_api', __name__)
login_api = Blueprint('login_api', __name__)


@join_api.route('/api/users', methods=['POST'])
def api_join():
    received = request.get_json()
    id_receive = received['id']
    pw_hash = get_encrypted_password(received['password'])

    mongodb().user.insert_one({'id': id_receive, 'password': pw_hash})

    return jsonify({'msg': '회원가입 성공'})


@id_check_api.route("/api/users", methods=['GET'])
def api_check_id():
    id_receive = request.args.get('id')
    user_by_id = mongodb().user.find_one({'id': id_receive})
    if user_by_id is not None:
        return jsonify({'msg': '이미존재하는 아이디입니다..', 'available': False})
    else:
        return jsonify({'msg': '사용가능한 아이디입니다.', 'available': True})


@login_api.route("/api/users/login", methods=['POST'])
def api_login():
    id_receive = request.form['id']
    pw_receive = request.form['password']
    pw_hash = get_encrypted_password(pw_receive)
    result = mongodb().user.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        token = jwt.encode(payload, get_secret_key(), algorithm='HS256')
        resp = make_response(jsonify({'result': 'success', 'token': token, 'msg': '인증 성공'}))
        resp.set_cookie('accessToken', token)
        return resp
    else:
        return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호를 확인하세요'})


@login_api.route("/api/users/auth", methods=['GET'])
def api_auth():
    token_receive = request.cookies.get('accessToken')
    try:
        payload = jwt.decode(token_receive, get_secret_key(), algorithms=['HS256'])
        userinfo = mongodb().user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


def get_encrypted_password(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()


def get_secret_key():
    dotenv_path = Path('.env')
    load_dotenv(dotenv_path=dotenv_path)
    return os.getenv('SECRET_KEY')
