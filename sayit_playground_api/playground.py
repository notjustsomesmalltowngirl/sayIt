import os
from flask import Flask, render_template, jsonify, request
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
from models import db, Playground, DidYouKnow, Hypotheticals, HotTakes, NeverHaveIEver
from models import WouldYouRather, StoryBuilder, Riddle, TwoTruthsAndALie
from models import User, PendingSuggestions
from sqlalchemy.sql.expression import func
from utils.helpers import get_game_by_type, return_error_for_wrong_params, get_game_to_type_mapping

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


# with app.app_context():
#     game_type = 'did_you_knows'
#     game = Playground.query.filter_by(type='did you know').scalar()
#     query = getattr(game, game_type)
#     print(query.order_by(func.random()).limit(1).one().to_dict())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/v1/all_game_types', methods=['GET'])
def get_all_game_types():
    all_games = Playground.query.all()
    return jsonify(
        {
            'all_games': [g.type for g in all_games]
        }
    ), 200


@app.route('/api/v1/get_random', methods=['GET'])
def get_random_game():
    game_type = request.args.get('game_type')
    error_response = return_error_for_wrong_params(game_type)
    if error_response:
        error, status_code = error_response
        return jsonify(error), status_code
    type_ = get_game_to_type_mapping(game_type)
    game = Playground.query.filter_by(type=game_type.lower()).scalar()
    query = getattr(game, type_)
    return jsonify(
        {
            game_type: query.order_by(func.random()).limit(1).one().to_dict()
        }
    )


@app.route('/api/v1/get', methods=['GET'])
def get_by_type():
    game_type = request.args.get('game_type')
    limit = request.args.get('limit')
    category = request.args.get('category')
    error_response = return_error_for_wrong_params(game_type)
    if error_response:
        error, status_code = error_response
        return jsonify(error), status_code
    game = Playground.query.filter_by(type=game_type.lower()).scalar()
    match game_type.lower():
        case 'did you know':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), DidYouKnow,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'hypotheticals':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), Hypotheticals,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'hot takes':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), HotTakes,
                                                   category=category, limit=limit)
            return jsonify(result), status_code
        case 'never have i ever':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), NeverHaveIEver,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'would you rather':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), WouldYouRather,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'story builder':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), StoryBuilder,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'riddles':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), Riddle, category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        case 'two truths and a lie':
            result, status_code = get_game_by_type(game, get_game_to_type_mapping(game_type), TwoTruthsAndALie,
                                                   category=category,
                                                   limit=limit)
            return jsonify(result), status_code
        # default's been handled


@app.route('/api/v1/add', methods=['GET', 'POST'])
def suggest_new_game():
    if request.method == 'POST':
        ...
    return render_template('pending_suggestions.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ...
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ...
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    ...


if __name__ == "__main__":
    app.run(debug=True)
