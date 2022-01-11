from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.userinfo

# 비밀번호를 해쉬태그로 변환할때 필요한 라이브러리
import hashlib

# 테스트용 메인페이지 접속
@app.route('/')
def home():
    return render_template('test.html')

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
    app.run('0.0.0.0', port=5000, debug=True)