import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(str(tmp_path / "test.db")))


def reading(rate=120.0, ts="2026-01-01T12:00:00", channel=0):
    return {"timestamp": ts, "channel": channel, "count_rate": rate}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_valid_reading_is_stored(client):
    assert client.post("/readings", json=reading()).status_code == 201
    stored = client.get("/readings").json()
    assert len(stored) == 1
    assert stored[0]["count_rate"] == 120.0


def test_out_of_range_reading_is_rejected_and_not_stored(client):
    resp = client.post("/readings", json=reading(rate=5000.0))
    assert resp.status_code == 422
    assert client.get("/readings").json() == []


def test_bad_channel_is_rejected(client):
    assert client.post("/readings", json=reading(channel=99)).status_code == 422


def test_gaps_endpoint_reports_missing_data(client):
    client.post("/readings", json=reading(ts="2026-01-01T12:00:00"))
    client.post("/readings", json=reading(ts="2026-01-01T12:00:30"))
    gaps = client.get("/gaps", params={"channel": 0, "max_gap_s": 5}).json()
    assert len(gaps) == 1
    assert gaps[0]["seconds"] == 30
