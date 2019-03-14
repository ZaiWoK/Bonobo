from .app import app, db
from flask import render_template, url_for, redirect, request, flash
from .models import get_books, have_books, get_book, get_books_for_author, get_sample, get_authors, get_author, Author, User
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256

@app.route("/")
def home():
    return render_template("home.html",title="Hello world", books=get_sample())

@app.route("/books")
def books():
    return render_template("books.html",title="All books", books=get_books())    

@app.route("/authors")
def authors():
    return render_template("authors.html",title="Authors", authors=get_authors())

@app.route("/book/<int:index>")
def book(index):
    return render_template(
        "book.html",
        book=get_book(index))

@app.route("/book/<author>")
def author_sort(author):
    return get_books_for_author(author)

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name = a.name)
    return render_template("edit-author.html", author = a, form =f)

@app.route("/save/author/", methods =("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('author', index = a.id))
    a = get_author(int(f.id.data))
    return render_template("edit-author.html", author = a, form = f)

class NewAuthorForm(FlaskForm):
    name = StringField('Nom', validators = [DataRequired()])

@app.route("/new/author")
@login_required
def new_author():
    f = NewAuthorForm(name = None)
    return render_template("new-author.html", form = f)

@app.route("/save/newAuthor/", methods =("POST",))
def save_newAuthor():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        flash('Cet auteur est déjà enregistré sur le site')
        authors = get_authors()
        a = Author(name=f.name.data)
        for author in authors:
            if a.name == author.name :
                flash('Cet auteur est déjà enregistré sur le site')
                return redirect(url_for("new-author", form = AuthorForm()))
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('author', index = a.id))
    return render_template("new-author.html", form = f)

class DeleteAuthorForm(FlaskForm):
    id = HiddenField('id')

@app.route("/author/<int:index>")
def author(index):
    author=get_author(index)
    f = DeleteAuthorForm(id = index)
    return render_template(
        "author.html",
        title="Author "+str(index),
        author=get_author(index),
        books=get_books_for_author(index), form = f)

@app.route("/delete/author/", methods =("POST",))
@login_required
def delete_author():
    author = None
    f = DeleteAuthorForm()
    id = int(f.id.data)
    if f.validate_on_submit():
        author=get_author(id)
        if have_books(id):
            books=get_books_for_author(id)
            for x in books:
                db.session.delete(x)
                db.session.commit()
        db.session.delete(author)
        db.session.commit()
        return redirect(url_for('authors'))
    return render_template(
        "author.html",
        title="Author "+str(id),
        author=get_author(id),
        books=get_books_for_author(id), form = f)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))