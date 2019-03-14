import yaml
import os.path
import random
from .app import db, login_manager
from flask_login import UserMixin

BOOKS = yaml.load(open(os.path.join(os.path.dirname(__file__),"data.yml")))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    url = db.Column(db.String(200))
    img = db.Column(db.String(100))
    title = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))
    
    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)
        

def get_sample():
    return Book.query.limit(10).all()

def get_books(n=None):
    return Book.query.all()

def get_book(index):
    return Book.query.get_or_404(index)

def get_books_for_author(id):
    return Author.query.get(id).books.all()

def get_authors():
    return Author.query.all()

def get_author(id):
    return Author.query.get(id)

def have_books(id):
    return get_books_for_author(id)!=None

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)