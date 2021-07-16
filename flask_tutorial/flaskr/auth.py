import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import (
    check_password_hash, generate_password_hash
)
from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

# Main views needed: register, log in, log out

@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # request.form is a special dict, mapping submitted keys/values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
    
        # Validation
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} already exists.'
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # Shouldn't give away if its password or user...should we?
        # Either way, easy to split this up if needed.
        if (user is None) or not (check_password_has(user['password'], password)):
            error = 'Incorrect username or password.'

        # session is a dict stored across requests - a cookie.
        # This can be checked for user-specific information being available.
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# This registers a fn that runs before view, no matter what url is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get['user_id']
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view
