from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow()

class UsersSchema(ma.Schema):
    id = fields.String()
    user_id = fields.String()
    pw = fields.String()
    nickname = fields.String()
    #address = fields.String()
    #address_gu = fields.String()
    #address_dong = fields.String()
    #lat_long = fields.String()
    lat = fields.String()
    long = fields.String()

class BooksSchema(ma.Schema):

    book_id = fields.String()
    title = fields.String()
    author_id = fields.String()
    image_url = fields.String()
    description = fields.String()
    average_rating = fields.String()