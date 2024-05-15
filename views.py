from flask import render_template, jsonify, request
from . import app, db
from .models import User
from .models import Move 
from .calcrank import update_ratings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/api/user/<int:user_id>')
def api_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        "username": user.username,
        "rating": user.rating,
        "total_games": user.total_games,
        "total_moves": user.total_moves,
        "wins": user.wins,
        "losses": user.losses
    }
    return jsonify(user_data)

@app.route('/record_move', methods=['POST'])
def record_move():
    game_id = request.form['game_id']
    player_id = request.form['player_id']
    position = request.form['position']
    move_number = request.form['move_number']

    new_move = Move(game_id=game_id, player_id=player_id, position=position, move_number=move_number)
    db.session.add(new_move)
    db.session.commit()

    return jsonify({"message": "Move recorded successfully"})


@app.route('/game_complete', methods=['POST'])
def game_complete():
    try:
        winner_id = int(request.form['winner_id'])
        loser_id = int(request.form['loser_id'])

        winner = User.query.get_or_404(winner_id)
        loser = User.query.get_or_404(loser_id)

        # Update game stats
        winner.wins += 1
        loser.losses += 1
        winner.total_games += 1
        loser.total_games += 1

        # Update ratings
        update_ratings(winner, loser)

        db.session.commit()

        return jsonify({"message": "Game results updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
