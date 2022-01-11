from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('localhost', 27017)
db = client.userinfo



# 테스트용 메인페이지 접속
#### 추후에 페이지 병합할 때 삭제하거나 mainpage접속 코드로 변경해야합니다!! ####

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

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
# id와 pw, nickname을 받아서 mongoDB에 저장.
# 저장하기 전에 pw를 sha256 방법(=단방향 암호화. 받은 사람이 풀어볼 수 없음.)으로 암호화해서 저장함.
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
