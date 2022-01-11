from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# client = MongoClient('mongodb://test:test@13.125.48.221/.dbmini')
client = MongoClient('localhost', 27017)
db = client.dbmini


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('1.happy-기쁨.html')


# API 역할을 하는 부분
@app.route('/api/sub', methods=['GET'])
def happy():
    mlist = list(db.happy_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})

@app.route('/review', methods=['POST'])
def saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment' : comment_receive
    }
    db.review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})


@app.route('/review', methods=['GET'])
def review():
    review = list(db.review.find({}, {'_id': False}))
    return jsonify({'review_list' : review})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)