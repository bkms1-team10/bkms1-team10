from sqlalchemy import Sequence
from werkzeug.security import check_password_hash, generate_password_hash
from base import db

class Users(db.Model):

    id = db.Column(db.String, primary_key=True)
    # id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(1000), nullable=True)
    pw = db.Column(db.String(1000), nullable=False)
    nickname = db.Column(db.String(1000), nullable=False)
    #address = db.Column(db.String(1000), nullable=True)
    email = db.Column(db.String(1000), nullable=True)
    #address_gu = db.Column(db.String(1000), nullable=True)
    #address_dong = db.Column(db.String(1000), nullable=True)
    #lat_long = db.Column(db.String(1000), nullable=True)
    lat = db.Column(db.String(1000), nullable=True)
    long = db.Column(db.String(1000), nullable=True)



class Books(db.Model):

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=True)
    author_id = db.Column(db.String(1000), nullable=True)
    image_url = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    average_rating = db.Column(db.String(1000), nullable=True)
