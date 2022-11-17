from flask import Blueprint, jsonify
from db_connect import mongodb

review_details_api = Blueprint('review_details_api', __name__)


@review_details_api.route('/api/reviews/<string:id>', methods=['GET'])
def review_get(id):
    review_list = mongodb().review.find_one({'id': int(id)}, {'_id': False})
    return jsonify({'review': review_list})
