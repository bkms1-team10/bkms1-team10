"""
DB
"""
SECRET_KEY = 'Test'

SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db/project.db'  #. Local DB

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 3600


