import os
import random
from datetime import timedelta, datetime

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from flask import Flask, render_template, url_for, session, redirect, request
from flask_session import Session
from flask_caching import Cache
from dotenv import load_dotenv
from helper_functions import get_username
from models import db, User, NewsItem, Remark
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

# app.config['CACHE_TYPE'] = 'SimpleCache'
# app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes
# cache = Cache(app)

with app.app_context():  # a global variable
    db.create_all()
    # current_user = User.query.filter_by(username=session['username']).first()
    #
    # all_news_items = NewsItem.query.all()
    # if all_news_items:
    #     news_item_by_category = db.session.query(NewsItem).filter_by(type='entertainment').all()
    #     for n in news_item_by_category:
    #         today_date = datetime.now().date()
    #         yesterday = today_date - timedelta(days=1)
    #         date_published = datetime.strptime(n.published_at, "%Y-%m-%d %H:%M:%S")
    #         if date_published.date() in [yesterday, today_date]:
    #             print({
    #                 'headline': n.headline,
    #                 'description': n.description,
    #                 'url': n.url
    #
    #             })


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
        return render_template('404.html', username=username)  #


@app.context_processor
def inject_globals():
    return dict(assign_username=assign_username,
                categories=['business', 'sports', 'entertainment', 'general', 'health', 'technology', ])


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


def fetch_article(category):
    all_news_items = NewsItem.query.all()
    if all_news_items:
        news_item_by_category = db.session.query(NewsItem).filter_by(type=category).all()
        if news_item_by_category:
            for n in news_item_by_category:
                print(f'fetching {category} from db not API')
                today_date = datetime.now().date()
                yesterday = today_date - timedelta(days=1)
                date_published = datetime.strptime(n.published_at, "%Y-%m-%d %H:%M:%S")
                if date_published.date() in [today_date, yesterday]:
                    return {
                        'headline': n.headline,
                        'description': n.description,
                        'url': n.url

                    }
    print(f'Fetching {category} from API not DB')
    top_headlines_url = 'https://newsapi.org/v2/top-headlines?'
    params = {
        'apiKey': os.getenv('NEWS_API_KEY'),
        'category': category,
    }
    try:
        response = requests.get(top_headlines_url, params).json()
    except (ConnectionError, Timeout):
        return {
            'headline': 'Unable to fetch headline',
            'description': 'Please check your internet connection.',
            'url': '#'
        }
    articles = response.get('articles', [])
    article = articles[0] if articles else {'title': 'No headline available', 'description': '', 'url': '#'}
    headline = article['title']
    description = article['description'] if article['description'] else 'No description available'
    url = article['url'] if article['url'] else '#'
    published_at = article['publishedAt'].split('T')[0]

    new_news_item = NewsItem(type=category, headline=headline, description=description,
                             url=url, published_at=datetime.strptime(published_at, "%Y-%m-%d"))

    db.session.add(new_news_item)
    db.session.commit()
    print(new_news_item.published_at, new_news_item.created_at)
    return {
        'headline': headline,
        'description': description,
        'url': url
    }


@app.route('/discussions/<category>', methods=['GET', 'POST'])
def goto_category(category):
    article_data = fetch_article(category)
    # if request.method == 'POST':
    #     comment = request.form.get('comment')
    news_item = NewsItem.query.filter_by(type=category).order_by(NewsItem.published_at.desc()).first()
    print(news_item.description)
    # new_comment = Remark(content=comment, user=current_user, )
    return render_template('discussions_with_jinja.html', article=article_data, category=category)


if __name__ == "__main__":
    app.run(debug=True)
