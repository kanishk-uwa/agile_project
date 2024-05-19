from flask import Flask

from sqlconnect import db, app, userinfo
from flask import render_template,request,flash
@app.route('/')
def hello_world():  # put application's code here
    return render_template('loginpage.html')

@app.route("/login", methods=['POST','GET' ])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not all([username, password]):
            flash('please fullfill all fields')
        get_user = db.session.query(userinfo.userid, userinfo.username,userinfo.pwd).filter(
            userinfo.username == username).first()
        if username==get_user.username and password==get_user.pwd:
            return render_template("welcome.html")
        elif get_user is None:
            return render_template("404.html")
    else:
        return render_template("404.html")
@app.route("/turn_to_register", methods=['POST','GET' ])
def turn_to_register():
    if request.method == 'POST':
        return render_template("register.html")

@app.route("/modify_user", methods=['POST', 'GET'])
def modify_user():
    if request.method == 'POST':
        return render_template("modify_user.html")

## 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not all([username, password, password2]):
            flash('please fullfill all fields')
        elif password != password2:
            flash('The two pwd are not same')
        else:
            new_user = userinfo()
            new_user.username = username
            new_user.pwd = password
            db.session.add(new_user)
            db.session.commit()
            return render_template("welcome.html")
    else:
        return render_template("404.html")

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        get_user = db.session.query(userinfo.userid, userinfo.username, userinfo.pwd).filter(
            userinfo.username == username).first()
        if username==get_user.username and password==get_user.pwd:
            if password!=password2:
                get_user.pwd = password2
                db.sessiion.commit()
                return render_template("welcome.html.html")
            else:
                flash('The two pwd are same')
        else:
            return render_template("404.html")
    else:
        return render_template("404.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)



# @app.route("/")
# def find_all_users():
#     user1 = userinfo.query.all()
#     print(user1)
#     return render_template("list.html", user1=user1)
#


#
#
# ## 登录
# # @app.route('/login/', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form.get('username')
# #         password = request.form.get('password')
# #         if not all([username, password]):
# #             flash('参数不完整')
# #         user = userinfo.query.filter(userinfo.username == username, userinfo.pwd == password).first()
# #         print(user.username)
# #         print(user.password)
# #         if user:
# #             return '登录成功'
# #         else:
# #             return "login fail"
# #     return render_template('login.html')
#
#
# if __name__ == '__main__':
#     app.run()
