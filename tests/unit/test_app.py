import pytest

from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_calc_ok(client):
    res = client.get("/calc/add?a=2&b=3")
    assert res.status_code == 200
    assert res.get_json()["result"] == 5


def test_calc_unknown_op(client):
    assert client.get("/calc/pow?a=2&b=3").status_code == 404


def test_calc_missing_params(client):
    assert client.get("/calc/add?a=2").status_code == 400


def test_calc_divide_by_zero(client):
    assert client.get("/calc/divide?a=1&b=0").status_code == 422
