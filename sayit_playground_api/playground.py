import os
from flask import Flask, render_template, jsonify, request
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from dotenv import load_dotenv
from models import db, Playground
app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)


with app.app_context():
    db.create_all()


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


@app.route('/api/v1/get', methods=['GET'])
def get_by_type():
    game_type = request.args.get('game_type')
    if not game_type:
        return jsonify({
            'error': {
                'Bad Request': "Missing 'game_type' in query parameters."
            }
        }), 400
    valid_types = ['did you know', 'hypotheticals', 'hot takes', 'never have I ever', 'would you rather',
                                 'story builder', 'riddles', 'two truths and a lie']
    if game_type.lower() not in valid_types:
        return jsonify({
            'error': {
                'Unprocessable Entity': f"{game_type} is not a valid game type . Valid options are: {', '.join([t.title() for t in valid_types])}"

            }
        }), 422
    game = Playground.query.filter_by(type=game_type).scalar()
    match game_type.lower():
        case 'did you know':
            return jsonify({
                game_type: [
                    d.to_dict() for d in game.did_you_knows
                ]
            }), 200
        case 'hypotheticals':
            return jsonify({
                game_type: [
                    h.to_dict() for h in game.hypotheticals
                ]
            }), 200
        case 'hot takes':
            return jsonify({
                game_type: [
                    h.to_dict() for h in game.hot_takes
                ]
            }), 200
        case 'never have I ever':
            return jsonify({
                game_type: [
                    n.to_dict() for n in game.never_have_i_evers
                ]
            }), 200
        case 'would you rather':
            return jsonify({
                game_type: [
                    w.to_dict() for w in game.would_you_rather_questions
                ]
            }), 200
        case 'story builder':
            return jsonify({
                game_type: [
                    s.to_dict() for s in game.story_builders
                ]
            }), 200
        case 'riddles':
            return jsonify({
                game_type: [
                    r.to_dict() for r in game.riddles
                ]
            }), 200
        case 'two truths and a lie':
            return jsonify({
                game_type: [
                    t.to_dict() for t in game.two_truths_and_a_lie
                ]
            }), 200


if __name__ == "__main__":
    app.run(debug=True)
