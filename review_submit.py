from flask import Blueprint, jsonify, request, render_template

submit_api = Blueprint('submit_api', __name__)
from db_connect import mongodb
import jwt
from user import get_secret_key


@submit_api.route('/api/reviews', methods=['POST'])
def review_submit():
    token_receive = request.cookies.get('accessToken')
    payload = jwt.decode(token_receive, get_secret_key(), algorithms=['HS256'])
    userinfo = mongodb().user.find_one({'id': payload['id']}, {'_id': 0})
    if userinfo is None:
        return jsonify({'msg': '로그인이 필요합니다!', 'result': 'fail'})

    user_id = userinfo['id']

    star_receive = request.form['star_give']
    price_receive = request.form['price_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']

    doc = {
        'userId': user_id,
        'rating': star_receive,
        'price': price_receive,
        'title': title_receive,
        'comment': comment_receive
    }
    mongodb().review.insert_one(doc)
    return jsonify({'msg': '게시완료!', 'result': 'success'})
