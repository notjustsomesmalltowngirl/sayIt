import os
from datetime import timedelta
from flask import Flask, render_template, url_for, session, redirect
from flask_session import Session
from dotenv import load_dotenv
from helper_functions import get_username
from models import db, User

load_dotenv()
app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
db.init_app(app)
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(days=366)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# with app.app_context():
#     db.create_all()


@app.route('/get-username')
def assign_username():
    username, username_is_available = get_username()
    if username_is_available:
        session['username'] = username
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return username  # TODO: add a page for error handling that would be displayed to user in absence of usernames


@app.context_processor
def inject_globals():
    return dict(assign_username=assign_username, categories=['music', 'politics', 'sports', 'arts'])


@app.route('/')
def home():
    username = session.get('username', None)
    # user = db.session.query(User).filter_by(username=username).first()
    # print(user)
    return render_template('index_with_jinja.html', username=username)


@app.route('/discussions')
def show_discussions_page():
    return render_template('discussions_with_jinja.html')


@app.route('/<category>')
def goto_category(category):
    return redirect(url_for('home'))  # TODO: add real logic here, maybe call an api that return stuff about each category


if __name__ == "__main__":
    app.run(debug=True)
