from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    rating = db.Column(db.Integer, default=1000)
    total_games = db.Column(db.Integer, default=0)
    total_moves = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Accessing the password attribute directly is not allowed')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moves = db.relationship('Move', backref='game', lazy=True)

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    move_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(10), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))