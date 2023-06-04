from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
import base


class DefaultFlask(Flask):
    """
    Flask Setting
    """

    def __init__(self, **kwargs):
        Flask.__init__(self, __name__, **kwargs)
        base.app = self
        self.config.from_envvar('SETTINGS')
        
        # database
        # base.db = _BaseSQLAlchemy(base.app)
        base.db = _BaseSQLAlchemy(base.app, session_options={"autoflush": False})
        Migrate(base.app, base.db)
        # from . import views

app = None 

def init(**kwargs):
    """
    Setting Flask (call CorFlask)
    """
    global app
    if not app :
        app = DefaultFlask(**kwargs)

    # use logger
    return app

