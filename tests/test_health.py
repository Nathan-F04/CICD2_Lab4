#test_health.py
import pytest

def test_health(client):
    #makes a get request that should assert 200 and return a json format status
    result = client.get("/health")
    assert result.status_code == 200
    assert result.json() == {"status": "ok"}
