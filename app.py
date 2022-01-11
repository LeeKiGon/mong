from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/sub')
def sub():
    return render_template("sub.html")

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)