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
#payload로 부터 id를 꺼내와 실제 user의 정보를 읽어옴
@app.route('/main')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', nick=user_info["nick"])
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인을 해 주세요!"))

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
#flutter 크롤링데이터
@app.route('/api/flutter', methods=['GET'])
def flutter():
    mlist = list(db.flutter_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#worry 크롤링데이터
@app.route('/api/worry', methods=['GET'])
def worry():
    mlist = list(db.worry_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#cvs 크롤링데이터
@app.route('/api/cvs', methods=['GET'])
def cvs():
    mlist = list(db.cvs_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#sad 크롤링데이터
@app.route('/api/sad', methods=['GET'])
def sad():
    mlist = list(db.sad_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#comfort 크롤링데이터
@app.route('/api/comfort', methods=['GET'])
def comfort():
    mlist = list(db.comfort_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#eht 크롤링데이터
@app.route('/api/eht', methods=['GET'])
def eht():
    mlist = list(db.eht_list.find({}, {'_id': False}))
    return jsonify({'mong_list': mlist})
#sleep 크롤링데이터
@app.route('/api/sleep', methods=['GET'])
def sleep():
    mlist = list(db.sleep_list.find({}, {'_id': False}))
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
#flutter 리뷰 입력받기
@app.route('/api/flutter_review', methods=['POST'])
def flutter_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.flutter_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#worry 리뷰 입력받기
@app.route('/api/worry_review', methods=['POST'])
def worry_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.worry_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#cvs 리뷰 입력받기
@app.route('/api/cvs_review', methods=['POST'])
def cvs_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.cvs_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#sad 리뷰 입력받기
@app.route('/api/sad_review', methods=['POST'])
def sad_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.sad_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#comfort 리뷰 입력받기
@app.route('/api/comfort_review', methods=['POST'])
def comfort_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.comfort_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#eht 리뷰 입력받기
@app.route('/api/eht_review', methods=['POST'])
def eht_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.eht_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#sleep 리뷰 입력받기
@app.route('/api/sleep_review', methods=['POST'])
def sleep_saving():
    comment_receive = request.form['comment_give']
    doc = {
        'comment': comment_receive
    }
    db.sleep_review.insert_one(doc)
    return jsonify({'msg': '저장 되었습니다!'})
#happy 리뷰 보여주기
@app.route('/api/happy_review2', methods=['GET'])
def happy_review():
    review = list(db.happy_review.find({}, {'_id': False}))
    return jsonify({'happyreview_list': review})
#flutter 리뷰 보여주기
@app.route('/api/flutter_review2', methods=['GET'])
def flutter_review():
    review = list(db.flutter_review.find({}, {'_id': False}))
    return jsonify({'flutterreview_list': review})
#worry 리뷰 보여주기
@app.route('/api/worry_review2', methods=['GET'])
def worry_review():
    review = list(db.worry_review.find({}, {'_id': False}))
    return jsonify({'worryreview_list': review})
#cvs 리뷰 보여주기
@app.route('/api/cvs_review2', methods=['GET'])
def cvs_review():
    review = list(db.cvs_review.find({}, {'_id': False}))
    return jsonify({'cvsreview_list': review})
#sad 리뷰 보여주기
@app.route('/api/sad_review2', methods=['GET'])
def sad_review():
    review = list(db.sad_review.find({}, {'_id': False}))
    return jsonify({'sadreview_list': review})
#comfort 리뷰 보여주기
@app.route('/api/comfort_review2', methods=['GET'])
def comfort_review():
    review = list(db.comfort_review.find({}, {'_id': False}))
    return jsonify({'comfortreview_list': review})
#eht 리뷰 보여주기
@app.route('/api/eht_review2', methods=['GET'])
def eht_review():
    review = list(db.eht_review.find({}, {'_id': False}))
    return jsonify({'ehtreview_list': review})
#sleep 리뷰 보여주기
@app.route('/api/sleep_review2', methods=['GET'])
def sleep_review():
    review = list(db.sleep_review.find({}, {'_id': False}))
    return jsonify({'sleepreview_list': review})
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
#flutter 리뷰 삭제하기
@app.route('/api/flutter_delete', methods=['POST'])
def flutter_delete():
    comment_receive = request.form['comment_give']
    db.flutter_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#anger 리뷰 삭제하기
@app.route('/api/anger_delete', methods=['POST'])
def anger_delete():
    comment_receive = request.form['comment_give']
    db.anger_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#worry 리뷰 삭제하기
@app.route('/api/worry_delete', methods=['POST'])
def worry_delete():
    comment_receive = request.form['comment_give']
    db.worry_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#worry 리뷰 삭제하기
@app.route('/api/cvs_delete', methods=['POST'])
def cvs_delete():
    comment_receive = request.form['comment_give']
    db.cvs_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#sad 리뷰 삭제하기
@app.route('/api/sad_delete', methods=['POST'])
def sad_delete():
    comment_receive = request.form['comment_give']
    db.sad_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#comfort 리뷰 삭제하기
@app.route('/api/comfort_delete', methods=['POST'])
def comfort_delete():
    comment_receive = request.form['comment_give']
    db.comfort_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#eht 리뷰 삭제하기
@app.route('/api/eht_delete', methods=['POST'])
def eht_delete():
    comment_receive = request.form['comment_give']
    db.eht_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})
#sleep 리뷰 삭제하기
@app.route('/api/sleep_delete', methods=['POST'])
def sleep_delete():
    comment_receive = request.form['comment_give']
    db.sleep_review.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})

##로딩페이지
@app.route('/')
def loading():
    return render_template("loading.html")

#happy 상세페이지 콜!
@app.route('/happy')
def happy_html():
    return render_template("happy.html")
#anger 상세페이지 콜!
@app.route('/anger')
def anger_html():
    return render_template("anger.html")
#flutter 상세페이지 콜!
@app.route('/flutter')
def flutter_html():
    return render_template("flutter.html")
#worry 상세페이지 콜!
@app.route('/worry')
def worry_html():
    return render_template("worry.html")
#cvs 상세페이지 콜!
@app.route('/cvs')
def cvs_html():
    return render_template("cvs.html")
#sad 상세페이지 콜!
@app.route('/sad')
def sad_html():
    return render_template("sad.html")
#comfort 상세페이지 콜!
@app.route('/comfort')
def comfort_html():
    return render_template("comfort.html")
#eht 상세페이지 콜!
@app.route('/eht')
def eht_html():
    return render_template("eht.html")
#sleep 상세페이지 콜!
@app.route('/sleep')
def sleep_html():
    return render_template("sleep.html")


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
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

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
    # subprocess.call('crawling.py', shell=True)
    app.run('0.0.0.0', port=5000, debug=True)
