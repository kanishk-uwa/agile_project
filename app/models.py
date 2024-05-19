from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the User table
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    rating = db.Column(db.Integer, default=1000)  # User rating, default is 1000
    total_games = db.Column(db.Integer, default=0)  # Total games played by the user
    total_moves = db.Column(db.Integer, default=0)  # Total moves made by the user
    wins = db.Column(db.Integer, default=0)  # Number of games won by the user
    losses = db.Column(db.Integer, default=0)  # Number of games lost by the user
    draws = db.Column(db.Integer, default=0)  # Number of games drawn by the user
    password_hash = db.Column(db.String(128))  # Hashed password

    @property
    def password(self):
        # Prevent password from being accessed directly
        raise AttributeError('Accessing the password attribute directly is not allowed')

    @password.setter
    def password(self, password):
        # Hash the password and store it in the password_hash field
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password
        return check_password_hash(self.password_hash, password)

# Define the Game model
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Game table
    moves = db.relationship('Move', backref='game', lazy=True)  # One-to-many relationship with the Move table

# Define the Move model
class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Move table
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))  # Foreign key referencing the Game table
    move_number = db.Column(db.Integer, nullable=False)  # Move number in the game
    position = db.Column(db.String(10), nullable=False)  # Position of the move on the game board
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key referencing the User table
