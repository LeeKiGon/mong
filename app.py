from flask import Flask, render_template


app = Flask(__name__)

# 페이지 이동
## 로딩페이지
@app.route('/')
def load():
    return render_template("loading.html")

@app.route('/main')
def main():
    return render_template("main.html")

##상세페이지
@app.route('/sub')
def sub():
    return render_template("sub.html")

##로그인페이지
@app.route('/login')
def register():
    return render_template('login.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)