import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tictactoe.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User, Game, Move

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
