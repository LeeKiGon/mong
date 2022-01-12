import subprocess

from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://test:test@13.125.48.221/.dbuserinfo')
# client = MongoClient('localhost', 27017)
db = client.dbuserinfo

##메인페이지
@app.route('/main')
def main():
    return render_template('main.html')

##상세페이지
# API 역할을 하는 부분
#happy 크롤링데이터
@app.route('/api/happy', methods=['GET'])
def happy():
    mlist = list(db.happy_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#anger 크롤링데이터
@app.route('/api/anger', methods=['GET'])
def anger():
    mlist = list(db.anger_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#happy 리뷰 입력받기
@app.route('/api/happy_review', methods=['POST'])
def happy_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.happy_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#happy 리뷰 보여주기
@app.route('/api/happy_review2', methods=['GET'])
def happy_review():
    review = list(db.happy_review.find({}, {'_id': False}))
    return jsonify({'happyreview_list': review})

#anger 리뷰 입력받기
@app.route('/api/anger_review', methods=['POST'])
def anger_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.anger_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#anger 리뷰 보여주기
@app.route('/api/anger_review2', methods=['GET'])
def anger_review():
    review = list(db.anger_review.find({}, {'_id': False}))
    return jsonify({'angerreview_list': review})

#happy 리뷰 삭제하기
@app.route('/api/happy_delete', methods=['POST'])
def happy_delete():
    comment_receive = request.form['comment_give']
    db.happy_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#anger 리뷰 삭제하기
@app.route('/api/anger_delete', methods=['POST'])
def anger_delete():
    comment_receive = request.form['comment_give']
    db.anger_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})

##로딩페이지
@app.route('/')
def loading():
    return render_template("loading.html")

@app.route('/happy')
def happy_html():
    return render_template("happy.html")

@app.route('/anger')
def anger_html():
    return render_template("anger.html")

#payload로 부터 id를 꺼내와 실제 user의 정보를 읽어옴
@app.route('/loading')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('login.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)


# [로그인 API}
# id, pw 받아서 맞춰보고 토큰 만들어 발급
@app.route('/api/login', methods=['POST'])
def api_login():
     # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # pw를 암호화화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    # id, 암화된 pw 가지고 해당 유저 찾기
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰 만들어 발급
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY)

        # token 전달
        return jsonify({'result': 'success', 'token': token})
        # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 로그인 페이지로 넘어갑니다.
@app.route('/register')
def register():
    return render_template('register.html')


# [회원가입 API]
# id와 pw, nickname을 받아서 mongoDB에 저장합니다.
# 저장하기 전에 pw를 sha256 방법(=단방향 암호화. 받은 사람이 풀어볼 수 없습니다.)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})


# ID중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    userid_receive = request.form['userid_give']

    # DB에 유저가 사용하겠다고 입력한 ID와 같은 값이 있는지 찾아서
    # 있으면(전부 같은 값이면) true, 없으면(하나라도 다른 것이 있으면) false
    exists = bool(db.user.find_one({'id': userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 닉네임 중복확인
@app.route('/sign_up/check_dupnick', methods=['POST'])
def check_dupnick():
    usernick_receive = request.form['usernick_give']

    # DB에 유저가 사용하겠다고 입력한 닉네임과 같은 값이 있는지 찾아서
    # 있으면(전부 같은 값이면) true, 없으면(하나라도 다른 것이 있으면) false
    exists = bool(db.user.find_one({'nick': usernick_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    subprocess.call('crawling.py', shell=True)
    app.run('0.0.0.0', port=5000, debug=True)
