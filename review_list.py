from flask import Blueprint, jsonify
from db_connect import mongodb

review_list_api = Blueprint('review_list_api', __name__)


@review_list_api.route('/api/reviews', methods=['GET'])
def get_review_list():
    db_results = list(mongodb().review.find().sort([('_id', -1)]))
    response_list = []
    for db_result in db_results:
        thumbnail_image = 'undefined'
        if (len(db_result['images']) is not 0):
            thumbnail_image = db_result['images'][0]
        response_list.append({
            'id': db_result['id'],
            'title': db_result['title'],
            'rating': db_result['rating'],
            'thumbnailImage': thumbnail_image,
            'userId': db_result['userId']
        })
    return jsonify({'review': response_list, 'msg': '조회 성공!'})
