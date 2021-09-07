from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    # watchlists = db.relationship('Watchlist')

    @classmethod
    def signup(cls, username, email, password):
        hashed_pass = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=hashed_pass)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False

class Watchlist(db.Model):
    __tablename__ = 'watchlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.Text, unique=True)
    company_name = db.Column(db.Text, unique=True)
    stock_url = db.Column(db.Text)


class WatchlistStock(db.Model):
    __tablename__ = 'watchlist_stocks'
    
    watchlist_id = db.Column(db.Integer, db.ForeignKey('watchlists.id', ondelete='CASCADE'), primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id', ondelete='CASCADE'), primary_key=True)

def connect_db(app):
    db.app = app
    db.init_app(app)