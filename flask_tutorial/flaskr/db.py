import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# 'g' is a special object unique for each request.
# It's used to store data accessible by multiple functions during
# the request.
# Connection is stored + reused instead of being recreated if get_db
# is called again in same request.
# 'current_app' is similar, pointing to the Flask object handling the
# request; using an app factory means there is no object in the rest
# of the code.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
