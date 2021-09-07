import os
from flask import Flask, redirect, render_template, session, g, request, flash

from sqlalchemy.exc import IntegrityError

from models import db, connect_db
from forms import UserAddForm, LoginForm
from stocks import *

# test


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secretkey123")

connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    """Creates a user."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data
            )
            db.session.commit()

        except IntegrityError:
            return render_template('/signup.html', form=form)

        do_login(user)

        return redirect('/')

    else:
        return render_template('/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash('You have successfully logged in.', "success")
            return redirect('/')
        
        flash('Invalid credentials.', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle user logout."""

    do_logout()

    flash('You have been logged out.', 'success')

    return redirect('/login')

@app.route('/seed_data')
def seed_data():
    user = create_user('Avi', 'avi@a.com', '123')
    watchlist = create_watchlist('Test Watchlist 1', user.id)
    watchlist2 = create_watchlist('Test Watchlist 2', user.id)
    add_stock_to_watchlist('TEST', 'The Test Company', 'test_url', watchlist.id)
    add_stock_to_watchlist('TEST', 'The Test Company', 'test_url', watchlist2.id)

@app.route('/test')
def test():
    get_watchlist(1)

@app.route('/delete_test')
def delete_test():
    remove_stock_from_watchlist(1, 1)