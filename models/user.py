from sqlalchemy import Sequence
from werkzeug.security import check_password_hash, generate_password_hash
from base import db

class Users(db.Model):

    user_id = db.Column(db.String, primary_key=True)
    # id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id = db.Column(db.String(1000), nullable=True)
    pw = db.Column(db.String(1000), nullable=False)
    nickname = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(1000), nullable=True)
    email = db.Column(db.String(1000), nullable=True)
    address_gu = db.Column(db.String(1000), nullable=True)
    address_dong = db.Column(db.String(1000), nullable=True)
    lat_long = db.Column(db.String(1000), nullable=True)
    lat = db.Column(db.String(1000), nullable=True)
    long = db.Column(db.String(1000), nullable=True)
    ratings = db.relationship('Ratings', backref='user', lazy=True)
    sharings = db.relationship('Sharings', backref='user', lazy=True)


class Books(db.Model):

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=True)
    author_id = db.Column(db.String(1000), db.ForeignKey('authors.author_id'), nullable=True)
    image_url = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    average_rating = db.Column(db.String(1000), nullable=True)
    ratings = db.relationship('Ratings', backref='book', lazy=True)
    sharings = db.relationship('Sharings', backref='books', lazy=True)


class Authors(db.Model):
    author_id = db.Column(db.String(1000), primary_key=True, nullable=True)
    name = db.Column(db.String(1000), nullable=True)
    books = db.relationship('Books', backref='author', lazy=True)

class Ratings(db.Model):
    rating_id = db.Column(db.String(1000), primary_key=True)
    user_id = db.Column(db.String(1000), db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.String(1000), db.ForeignKey('books.book_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_id = db.Column(db.String(1000), db.ForeignKey('reviews.review_id'), nullable=True)

class Reviews(db.Model):
    review_id = db.Column(db.String(1000), primary_key=True)
    review_TEXT = db.Column(db.String(1000), nullable=False)
    ratings = db.relationship('Ratings', backref='review', lazy=True)

class Sharings(db.Model):
    user_id = db.Column(db.String(1000), db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.String(1000), db.ForeignKey('books.book_id'), primary_key=True)