from flask import Flask

app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
from flask_bootstrap import Bootstrap
Bootstrap(app)

import os.path

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../tuto.db'))
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "c40ef022-0e77-4c51-8491-6f3d1a1df73b"

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = "login"