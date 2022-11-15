from flask import Blueprint, jsonify, request, render_template
submit_api = Blueprint('submit_api', __name__)
from db_connect import mongodb


@submit_api.route('/review-submit', methods=['POST'])
def review_submit():
    star_receive = request.form['star_give']
    price_receive = request.form['price_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']

    doc = {
        'star': star_receive,
        'price': price_receive,
        'title': title_receive,
        'comment': comment_receive
    }
    mongodb().review.insert_one(doc)
    return jsonify({'msg': '게시완료!'})

