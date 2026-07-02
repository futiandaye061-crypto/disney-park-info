"""Thin client for the public queue-times.com API."""

from dataclasses import dataclass

import requests

BASE_URL = "https://queue-times.com"
REQUEST_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class Ride:
    name: str
    is_open: bool
    wait_time: int
    last_updated: str


def get_ride_wait_times(queue_times_id: int) -> list[Ride]:
    """Fetch current ride wait times for a park.

    `queue_times_id` is the park's id in the queue-times.com catalog.
    """
    url = f"{BASE_URL}/parks/{queue_times_id}/queue_times.json"
    response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    data = response.json()

    rides = list(data.get("rides", []))
    for land in data.get("lands", []):
        rides.extend(land.get("rides", []))

    return [
        Ride(
            name=ride["name"],
            is_open=ride["is_open"],
            wait_time=ride["wait_time"],
            last_updated=ride["last_updated"],
        )
        for ride in rides
    ]
