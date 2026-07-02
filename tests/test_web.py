from unittest.mock import patch

import pytest

from disney_park_info.api import Ride
from disney_park_info.web import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_index_lists_parks(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Tokyo Disneyland" in response.data


def test_status_endpoint_returns_404_for_unknown_park(client):
    response = client.get("/api/status/not-a-real-park")
    assert response.status_code == 404
    assert "Unknown park" in response.get_json()["error"]


@patch("disney_park_info.web.get_ride_wait_times")
def test_status_endpoint_returns_sorted_open_rides(mock_get_ride_wait_times, client):
    mock_get_ride_wait_times.return_value = [
        Ride(name="Short Wait Ride", is_open=True, wait_time=5, last_updated="2026-01-01T00:00:00Z"),
        Ride(name="Long Wait Ride", is_open=True, wait_time=60, last_updated="2026-01-01T00:00:00Z"),
        Ride(name="Closed Ride", is_open=False, wait_time=0, last_updated="2026-01-01T00:00:00Z"),
    ]

    response = client.get("/api/status/tokyo-disneyland")

    assert response.status_code == 200
    data = response.get_json()
    assert data["open_count"] == 2
    assert data["closed_count"] == 1
    assert [ride["name"] for ride in data["rides"]] == ["Long Wait Ride", "Short Wait Ride"]
