from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Move, Game
from .forms import LoginForm, RegistrationForm

# Create a blueprint for the main routes
main_blueprint = Blueprint('main', __name__)

# Route for the index page
@main_blueprint.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

# Route for user registration
@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            user = User(username=form.username.data, password=form.password.data)  # Uses the setter
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.index'))
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{error}", 'danger')
    return render_template('register.html', form=form)

# Route for user login
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Username not found. Please check and try again.', 'danger')
        elif not user.check_password(form.password.data):
            flash('Incorrect password. Please check and try again.', 'danger')
        else:
            login_user(user)
            return redirect(url_for('main.new_game'))
    else:
        flash('Invalid input. Please ensure all fields are correctly filled.', 'danger')
    return render_template('index.html', form=form)

# Route for user logout
@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

# Route for the user profile page
@main_blueprint.route('/profile')
@login_required
def profile():
    players = User.query.order_by(User.rating.desc()).limit(10).all()
    return render_template('profile.html', user=current_user, players=players)

# Route for the new game page
@main_blueprint.route('/new_game')
@login_required
def new_game():
    return render_template('new_game.html')

# Route to create a new game
@main_blueprint.route('/create_game')
@login_required
def create_game():
    game = Game()
    db.session.add(game)
    db.session.commit()
    flash('New game created! You can start playing.', 'success')
    return redirect(url_for('main.game_screen', game_id=game.id))

# Route to join an existing game
@main_blueprint.route('/join_game')
@login_required
def join_game():
    game = Game.query.filter(Game.moves == None).first()  # Join an active game with no moves
    if game:
        flash('Joined an existing game! You can start playing.', 'success')
        return redirect(url_for('main.game_screen', game_id=game.id))
    else:
        flash('No available games to join. Please create a new game.', 'danger')
        return redirect(url_for('main.new_game'))

# Route for the game screen
@main_blueprint.route('/game_screen/<int:game_id>')
@login_required
def game_screen(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game_screen.html', game=game)

# Route to submit a move
@main_blueprint.route('/submit_move', methods=['POST'])
@login_required
def submit_move():
    data = request.json
    game_id = data.get('game_id')
    move_number = data.get('move_number')
    position = data.get('position')

    move = Move(game_id=game_id, move_number=move_number, position=position, player_id=current_user.id)
    db.session.add(move)
    
    current_user.total_moves += 1
    db.session.commit()
    
    return jsonify({"message": "Move submitted successfully"})

# Route to update game results
@main_blueprint.route('/update_results', methods=['POST'])
def update_results():
    try:
        data = request.json
        user_id = data.get('user_id')
        result = data.get('result')

        user = User.query.get_or_404(user_id)

        if result == 'win':
            user.wins += 1
            user.rating += 25
        elif result == 'draw':
            user.draws += 1
        else:
            user.losses += 1
            user.rating -= 25
        
        user.total_games += 1

        opponent = User.query.filter(User.id != user_id).first()

        if result == 'win':
            opponent.losses += 1
            opponent.rating -= 25
        elif result == 'draw':
            opponent.draws += 1
        else:
            opponent.wins += 1
            opponent.rating -= 25
        
        opponent.total_games += 1

        db.session.commit()

        return jsonify({"message": "Game results updated successfully", "redirect": url_for('main.new_game')})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
