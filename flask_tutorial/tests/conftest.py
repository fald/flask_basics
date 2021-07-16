import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    # This creates + opens a temp file, returning descriptor and path.
    db_fd, db_path = tempfile.mkstemp()

    # Overriding the database path to point to temp (don't mess with production vals)
    # TESTING to True tells Flask to change some internal behavior for testing purposes
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Now we're using the temp stuff, init a db there.
    with app.app_context():
        init_db()
        get_db.executescript(_data_sql)

    yield app

    # Now close and remove temp stuff
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
