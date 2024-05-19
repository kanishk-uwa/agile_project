import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database
db = SQLAlchemy()

# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'  # Redirect to the login view if not authenticated

def create_app():
    # Create a new Flask application
    app = Flask(__name__)
    
    # Configure the SQLite database URI and secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tictactoe.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

    # Initialize the database and login manager with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Import the models to register them with SQLAlchemy
    from .models import User, Game, Move

    # Define the user loader callback for the login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register the main blueprint
    from .views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
