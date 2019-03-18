# coding: utf-8
import click
from .app import app, db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    db.create_all()

    import yaml
    persos = yaml.load(open(filename))

    from .models import Serie, Perso
    
    series = {}
    for p in persos :
        a = p["series"]
        if a not in series :
            o = Serie(name=a)
            db.session.add(o)
            series[a] = o
    db.session.commit()

    for p in persos:
        a = series[p["series"]]
        o = Perso(name = p["displayName"]["en_US"],
                 color = p["color"],
                 serie_id = a.id)
        db.session.add(o)
    db.session.commit()

@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()

@app.cli.command()
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    '''Adds a new user.'''
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username = username, password = m.hexdigest())
    db.session.add(u)
    db.session.commit()