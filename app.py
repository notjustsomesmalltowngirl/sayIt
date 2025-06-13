import os
import random
from datetime import timedelta, datetime
from flask import Flask, render_template, url_for, session, redirect
from flask_session import Session
from dotenv import load_dotenv
from helper_functions import get_username
from models import db, User
from sqlalchemy.exc import IntegrityError

load_dotenv()
app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
db.init_app(app)
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(days=366)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

with app.app_context():
    db.create_all()


@app.route('/get-username')
def assign_username():
    username, username_is_available = get_username()
    if username_is_available:
        session['username'] = username
        for _ in range(3):
            try:
                new_user = User(username=username)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('home'))
            except IntegrityError:  # incase uuid fails as a primary key and repeats itself
                db.session.rollback()
                with open('error_log.txt', 'a') as f:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Failed to create user '{username}'", file=f)
        return render_template('404.html')
    else:
        return render_template('404.html', username=username)


@app.context_processor
def inject_globals():
    return dict(assign_username=assign_username, categories=['music', 'politics', 'sports', 'arts', 'entertainment',
                                                             'general', 'business', 'health', 'technology', ])


@app.route('/')
def home():
    username = session.get('username', None)
    greetings = [
        'Hi', 'Hello', 'Welcome', 'Hey', 'Hi there', 'Yo!', "So glad you're here", 'What up!',
        'Step right in', 'You made it!',
        'Long time no see!', 'There you are!', 'Wassup!', 'Howdy!', 'Sup!',
        'Glad you showed up!', 'Fancy seeing you here!', 'You’re just in time!', 'Ayyy!'
    ]
    return render_template('index.html', greeting=random.choice(greetings), username=username)


@app.route('/discussions')
def goto_discussions():
    return render_template('discussions_with_jinja.html')


@app.route('/chatroom')
def goto_chatroom():
    return render_template('chatroom_with_jinja.html')


@app.route('/playground')
def goto_playground():
    return render_template('playground_with_jinja.html')


@app.route('/<category>')
def goto_category(category):
    return redirect(
        url_for('home'))  # TODO: use match statements to check for categories


if __name__ == "__main__":
    app.run(debug=True)
