# coding: utf-8
from .app import app, db
from flask import render_template, url_for, redirect, request, flash
from .models import get_persos, have_perso, get_perso, get_persos_for_serie, get_sample, get_series, get_serie, Serie, User
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256

@app.route("/")
def home():
    return render_template("home.html",title="Hello world", persos=get_sample())

@app.route("/persos")
def persos():
    return render_template("persos.html",title="All characters", persos=get_persos())    

@app.route("/series")
def series():
    return render_template("series.html",title="All series", series=get_series())

@app.route("/perso/<int:index>")
def perso(index):
    return render_template(
        "perso.html",
        perso=get_perso(index))

@app.route("/perso/<serie>")
def serie_sort(serie):
    return get_persos_for_serie(serie)

class SerieForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

@app.route("/edit/serie/<int:id>")
@login_required
def edit_serie(id):
    a = get_serie(id)
    f = SerieForm(id=a.id, name = a.name)
    return render_template("edit-serie.html", author = a, form =f)

@app.route("/save/serie/", methods =("POST",))
def save_serie():
    a = None
    f = SerieForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a = get_serie(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('serie', index = a.id))
    a = get_serie(int(f.id.data))
    return render_template("edit-serie.html", author = a, form = f)

class NewSerieForm(FlaskForm):
    name = StringField('Nom', validators = [DataRequired()])

@app.route("/new/serie")
@login_required
def new_serie():
    f = NewSerieForm(name = None)
    return render_template("new-serie.html", form = f)

@app.route("/save/newSerie/", methods =("POST",))
def save_newSerie():
    a = None
    f = SerieForm()
    if f.validate_on_submit():
        flash('Cette serie est déjà enregistrée sur le site')
        series = get_series()
        a = Serie(name=f.name.data)
        for serie in series:
            if a.name == author.name :
                flash('Cette serie est déjà enregistrée sur le site')
                return redirect(url_for("new-serie", form = SerieForm()))
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('serie', index = a.id))
    return render_template("new-serie.html", form = f)

class DeleteSerieForm(FlaskForm):
    id = HiddenField('id')

@app.route("/serie/<int:index>")
def serie(index):
    serie=get_serie(index)
    f = DeleteSerieForm(id = index)
    return render_template(
        "serie.html",
        title="Serie "+str(index),
        serie=get_serie(index),
        persos=get_persos_for_serie(index), form = f)

@app.route("/delete/serie/", methods =("POST",))
@login_required
def delete_serie():
    serie = None
    f = DeleteSerieForm()
    id = int(f.id.data)
    if f.validate_on_submit():
        serie=get_serie(id)
        if have_persos(id):
            persos=get_persos_for_serie(id)
            for x in persos:
                db.session.delete(x)
                db.session.commit()
        db.session.delete(serie)
        db.session.commit()
        return redirect(url_for('serie'))
    return render_template(
        "serie.html",
        title="Serie "+str(id),
        serie=get_serie(id),
        persos=get_persos_for_serie(id), form = f)

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