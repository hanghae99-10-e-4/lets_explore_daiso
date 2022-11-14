from flask import Blueprint, jsonify

exam_api = Blueprint('exam_api', __name__)


@exam_api.route('/api/exam', methods=['GET'])
def get_exam():
    return jsonify({'msg': 'get exam!'})
