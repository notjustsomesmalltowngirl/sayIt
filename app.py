
from flask import Flask, render_template, make_response, request
from helper_functions import get_username

app = Flask(__name__)


@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        print(username)
    else:
        print('username Is None')
    return render_template('index.html', username=username)


@app.route('/get-your-username')
def assign_username():
    existing_username = request.cookies.get('username')

    if existing_username:
        return f'Welcome back, {existing_username} 👋'

    new_username = get_username()
    response = make_response(f'New username assigned: {new_username}')
    response.set_cookie('username', new_username, max_age=60 * 60 * 24 * 366 * 2)
    return response


if __name__ == "__main__":
    app.run(debug=True)
