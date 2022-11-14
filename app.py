from flask import Flask, render_template
from db_connect import check_connection
from exam import exam_api

app = Flask(__name__)

### 이곳에 api를 등록하세요
app.register_blueprint(exam_api)


# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')


# 로그인 페이지
@app.route("/login")
def login():
    return render_template('login.html')


# 리뷰 상세 보기 페이지
@app.route('/review-details')
def review_details():
    return render_template('review-details.html')


# 리뷰 등록 페이지
@app.route('/review-submit')
def review_submit():
    return render_template('review-submit.html')


if __name__ == '__main__':
    ##### check database connection
    ##### db연결 여부를 확인하고자 한다면
    ##### 아래 주석 해제 후 앱 실행하여 db 연결 체크 후 다시 주석 처리하기
    # check_connection()
    app.run('0.0.0.0', port=5000, debug=True)
