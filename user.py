from flask import Blueprint, jsonify, request
import hashlib
from db_connect import mongodb

join_api = Blueprint('join_api', __name__)


@join_api.route('/api/users', methods=['POST'])
def api_join():
    received = request.get_json()
    id_receive = received['id']
    pw_hash = get_encrypted_password(received['password'])

    mongodb().user.insert_one({'id': id_receive, 'pw': pw_hash})

    return jsonify({'msg': '회원가입 성공'})


def get_encrypted_password(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()
