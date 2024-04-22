import os
import tempfile

import pytest
from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class ApiActions(object):
    def __init__(self, client):
        self._client = client

    def create(self,
                name='datacenter-1',
                metadata='{"monitoring": {"enabled": "true"},"limits": {"cpu": {"enabled": "true","value": "700m"}}}'
    ):
        return self._client.post(
            '/configs/',
            data={'name': name, 'metadata': metadata}
        )


    def get(self, url):
        return self._client.get(url)


@pytest.fixture
def api(client):
    return ApiActions(client)
