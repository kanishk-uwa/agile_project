from flask import Flask
import sqlite3

app = Flask(__name__)

def get_players():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, ranking, matches_won, image_url FROM players ORDER BY ranking ASC")
    players = cursor.fetchall()
    conn.close()
    return players

@app.route('/')
def index():
    players = get_players()
    return render_template('profile.html', players=players)


if __name__ == '__main__':
    app.run(debug=True)
