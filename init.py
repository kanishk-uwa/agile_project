from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tictactoe.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    # Will add code for log in sessions 
    return "Tic Tac Toe Game"

if __name__ == '__main__':
    app.run(debug=True)
