import pytest
from flask import g, session
from app.db import get_db


def test_create(client, app):
    response = client.post(
        '/configs/',
        data={
            'name': 'datacenter-1',
            'metadata': '{"monitoring": {"enabled": "true"},"limits": {"cpu": {"enabled": "true","value": "700m"}}}'}
    )

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM configs",
        ).fetchone() is not None


def test_get(client, api):
    assert client.get('/configs/datacenter-1').status_code == 200

    with client:
        api.get('/configs/datacenter-1')
        assert session['name'] == 'datacenter-1'
        assert session['metadata'] == \
            {"monitoring": {"enabled": "true"},"limits": {"cpu": {"enabled": "true","value": "700m"}}}
