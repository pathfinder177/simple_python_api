import pytest
from flask import session

def test_get(client, api):
    assert client.get('/search?metadata.monitoring.enabled=true').status_code == 200

    with client:
        api.get('/search?metadata.monitoring.enabled=true')
        assert session['name'] == 'datacenter-1'
        assert session['metadata'] == \
            {"monitoring": {"enabled": "true"},"limits": {"cpu": {"enabled": "true","value": "700m"}}}
