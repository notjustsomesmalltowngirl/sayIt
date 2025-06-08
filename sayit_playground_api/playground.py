import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from models import (db, Playground, DidYouKnow, HotTakes, WouldYouRather, NeverHaveIEver, Riddle, StoryBuilder,
                    TwoTruthsAndALie, Hypotheticals)

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)


# with app.app_context():
# db.create_all()


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


if __name__ == "__main__":
    app.run(debug=True)
