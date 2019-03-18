# coding: utf-8
import yaml
import os.path
import random
from .app import db, login_manager
from flask_login import UserMixin

BOOKS = yaml.load(open(os.path.join(os.path.dirname(__file__),"data.yml")))

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Serie (%d) %s>" % (self.id)

class Perso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    color = db.Column(db.String(7))
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.id"))
    serie = db.relationship("Serie", backref=db.backref("persos", lazy="dynamic"))
    
    def __repr__(self):
        return "<Perso (%d) %s>" % (self.id, self.name)
        

def get_sample():
    return Perso.query.limit(10).all()

def get_persos(n=None):
    return Perso.query.all()

def get_perso(index):
    return Perso.query.get_or_404(index)

def get_persos_for_serie(id):
    return Serie.query.get(id).persos.all()

def get_series():
    return Serie.query.all()

def get_serie(id):
    return Serie.query.get(id)

def have_perso(id):
    return get_persos_for_serie(id)!=None

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)