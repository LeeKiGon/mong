from flask import Flask, render_template


app = Flask(__name__)

# 페이지 이동
## 메인페이지
@app.route('/')
def main():
    return render_template("main.html")

##상세페이지
@app.route('/sub')
def sub():
    return render_template("sub.html")

##로그인페이지
@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)