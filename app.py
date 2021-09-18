import os
from flask import Flask, redirect, render_template, session, g, request, flash

from sqlalchemy.exc import IntegrityError

from models import db, connect_db
from forms import UserAddForm, LoginForm, NewWatchlistForm
from stocks import *


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

    return render_template('home.html', user_id=g.user)


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


@app.route('/new_watchlist', methods=['GET', 'POST'])
def new_watchlist():
    """Creates a new watchlist."""
    form = NewWatchlistForm()

    if form.validate_on_submit():
        name = form.name.data

        watchlist = create_watchlist(name=name, user_id=g.user.id)

        return redirect('/watchlists')


    return render_template('new_watchlist.html', form=form)


@app.route('/watchlists')
def show_watchlists():
    """Shows all of the user's watchlists."""
    if not g.user:
        flash("Access unauthorized - Please log in to see your watchlists.", "danger")
        
        return redirect("/login")

    watchlists = get_watchlists(user_id=g.user.id)

    return render_template('show_watchlists.html', watchlists=watchlists)


@app.route('/watchlists/<int:watchlist_id>')
def show_watchlist(watchlist_id):
    """Show a watchlist."""
    if not g.user:
        flash("Access unauthorized - Please log in to see your watchlist.", "danger")

        return redirect("/login")


    stocks = get_watchlist(watchlist_id=watchlist_id)
    watchlist = watchlist_name(watchlist_id=watchlist_id)

    return render_template('show_watchlist.html', stocks=stocks, watchlist=watchlist)


@app.route('/watchlists/<int:watchlist_id>/stock/<int:stock_id>', methods=['POST'])
def delete_stock(watchlist_id, stock_id):
    """Deletes a stock from a watchlist."""
    if not g.user:
        flash("Access unauthorized - Please log in.", "danger")

        return redirect('/login')

    stock = WatchlistStock.query.filter(WatchlistStock.stock_id == stock_id, WatchlistStock.watchlist_id == watchlist_id).first()
    
    db.session.delete(stock)
    db.session.commit()

    return redirect(f'/watchlists/{watchlist_id}')



@app.route('/seed_data')
def seed_data():
    watchlist = create_watchlist('Test Watchlist 1', g.user.id)
    watchlist2 = create_watchlist('Test Watchlist 2', g.user.id)
    add_stock_to_watchlist('TEST', 'The Test Company', watchlist.id)
    add_stock_to_watchlist('TEST', 'The Test Company', watchlist2.id)

@app.route('/test')
def test():
    get_watchlist(1)

@app.route('/delete_test')
def delete_test():
    remove_stock_from_watchlist(1, 1)