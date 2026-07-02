from unittest.mock import patch

from disney_park_info.api import Ride
from disney_park_info.cli import main


def test_list_command_shows_all_parks(capsys):
    exit_code = main(["list"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Tokyo Disneyland" in captured.out
    assert "Shanghai Disney Resort" in captured.out


def test_status_command_reports_unknown_park(capsys):
    exit_code = main(["status", "not-a-real-park"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Unknown park 'not-a-real-park'" in captured.err


@patch("disney_park_info.cli.get_ride_wait_times")
def test_status_command_shows_wait_times_sorted_by_congestion(mock_get_ride_wait_times, capsys):
    mock_get_ride_wait_times.return_value = [
        Ride(name="Short Wait Ride", is_open=True, wait_time=5, last_updated="2026-01-01T00:00:00Z"),
        Ride(name="Long Wait Ride", is_open=True, wait_time=60, last_updated="2026-01-01T00:00:00Z"),
        Ride(name="Closed Ride", is_open=False, wait_time=0, last_updated="2026-01-01T00:00:00Z"),
    ]

    exit_code = main(["status", "tokyo-disneyland"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Open: 2  Closed: 1" in captured.out
    long_wait_index = captured.out.index("Long Wait Ride")
    short_wait_index = captured.out.index("Short Wait Ride")
    assert long_wait_index < short_wait_index
    assert "Closed Ride" not in captured.out
