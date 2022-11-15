from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.2upl7qi.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/review-submit", methods=["POST"])
def review_submit():
    star_receive = request.form['star_give']
    price_receive = request.form['price_give']
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']

    doc = {
        'star':star_receive,
        'price':price_receive,
        'title':title_receive,
        'comment':comment_receive
    }
    db.daiso.insert_one(doc)
    return jsonify({'msg': '게시완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)