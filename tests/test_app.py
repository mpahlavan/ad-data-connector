"""Endpoint tests with the upstream ad API mocked out, so they run offline."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
os.environ["BASE_URL"] = "https://upstream.test"
os.environ["AUTH_TOKEN"] = "test-token"

import app as app_module  # noqa: E402
from utils import respond  # noqa: E402

AUTH = {"Authorization": "Bearer test-token"}


class FakeResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
        self.text = str(payload)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise respond.requests.exceptions.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._payload


@pytest.fixture
def client(monkeypatch):
    app_module.AUTH_TOKEN = "test-token"
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def mock_upstream(monkeypatch, payload, status=200):
    calls = []

    def fake_get(url, headers=None, params=None):
        calls.append({"url": url, "headers": headers, "params": params})
        return FakeResponse(payload, status)

    monkeypatch.setattr(respond.requests, "get", fake_get)
    return calls


def test_rejects_missing_token(client):
    assert client.get("/api/accounts").status_code == 403


def test_rejects_wrong_token(client):
    r = client.get("/api/accounts", headers={"Authorization": "Bearer nope"})
    assert r.status_code == 403


def test_accounts_are_renamed_to_public_shape(client, monkeypatch):
    calls = mock_upstream(monkeypatch, {"data": [{"id": "a1", "name": "Account1"}]})
    r = client.get("/api/accounts", headers=AUTH)
    assert r.status_code == 200
    assert r.get_json() == [{"accountName": "Account1", "accountId": "a1"}]
    assert calls[0]["url"].endswith("/demo/adAccounts")


def test_ad_data_requires_all_query_params(client):
    r = client.get("/api/adData?accountId=a1&start=2024-05-01", headers=AUTH)
    assert r.status_code == 400


def test_ad_data_is_returned_as_columns_and_rows(client, monkeypatch):
    rows = [
        {"campaign_id": "c1", "clicks": 21, "date": "2024-05-01"},
        {"campaign_id": "c2", "clicks": 31, "date": "2024-05-01"},
    ]
    calls = mock_upstream(monkeypatch, {"data": rows})
    r = client.get("/api/adData?accountId=a1&start=2024-05-01&end=2024-05-31", headers=AUTH)
    assert r.status_code == 200
    assert r.get_json() == {
        "columns": ["campaign_id", "clicks", "date"],
        "rows": [["c1", 21, "2024-05-01"], ["c2", 31, "2024-05-01"]],
    }
    assert calls[0]["params"] == {"start": "2024-05-01", "end": "2024-05-31"}


def test_empty_ad_data(client, monkeypatch):
    mock_upstream(monkeypatch, {"data": []})
    r = client.get("/api/adData?accountId=a1&start=2024-05-01&end=2024-05-31", headers=AUTH)
    assert r.get_json() == {"columns": [], "rows": []}


def test_upstream_error_is_passed_through(client, monkeypatch):
    mock_upstream(monkeypatch, {"error": "denied"}, status=401)
    r = client.get("/api/accounts", headers=AUTH)
    assert r.status_code == 401
    assert "error" in r.get_json()


def test_unknown_route_returns_json_404(client):
    r = client.get("/nope")
    assert r.status_code == 404
    assert r.get_json() == {"error": "Endpoint not found"}
