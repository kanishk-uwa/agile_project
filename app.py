from flask import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('loginpage.html')

@app.route("/login", methods=['POST','GET' ])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username=='123' and password=='456':
            return render_template("welcome.html")
        else:
            return render_template("404.html")
    else:
        return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)
