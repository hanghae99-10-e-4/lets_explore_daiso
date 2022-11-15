from flask import Blueprint, jsonify, request
import hashlib
from db_connect import mongodb

join_api = Blueprint('join_api', __name__)
id_check_api = Blueprint('id_check_api', __name__)


@join_api.route('/api/users', methods=['POST'])
def api_join():
    received = request.get_json()
    id_receive = received['id']
    pw_hash = get_encrypted_password(received['password'])

    mongodb().user.insert_one({'id': id_receive, 'pw': pw_hash})

    return jsonify({'msg': '회원가입 성공'})


@id_check_api.route("/api/users", methods=['GET'])
def api_check_id():
    id_receive = request.args.get('id')
    user_by_id = mongodb().user.find_one({'id': id_receive})
    if user_by_id is not None:
        return jsonify({'msg': '이미존재하는 아이디입니다..', 'available': False})
    else:
        return jsonify({'msg': '사용가능한 아이디입니다.', 'available': True})


def get_encrypted_password(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()
