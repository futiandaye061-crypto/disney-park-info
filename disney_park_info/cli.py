"""Command line interface for disney-park-info."""

import argparse
import sys
from itertools import groupby

from disney_park_info.api import get_ride_wait_times
from disney_park_info.parks import PARKS, get_park

MAX_BAR_LENGTH = 40


def _print_park_list() -> None:
    parks_by_country = groupby(sorted(PARKS, key=lambda p: p.country), key=lambda p: p.country)
    for country, parks in parks_by_country:
        print(f"{country}:")
        for park in parks:
            print(f"  {park.key:<32} {park.name}")


def _print_park_status(park_key: str) -> int:
    try:
        park = get_park(park_key)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    rides = get_ride_wait_times(park.queue_times_id)
    if not rides:
        print(f"No ride data available for {park.name}.")
        return 0

    open_rides = [ride for ride in rides if ride.is_open]
    closed_count = len(rides) - len(open_rides)
    average_wait = sum(ride.wait_time for ride in open_rides) / len(open_rides) if open_rides else 0

    print(f"{park.name} ({park.country})")
    print(f"Open: {len(open_rides)}  Closed: {closed_count}  Average wait: {average_wait:.0f} min\n")

    max_wait = max((ride.wait_time for ride in open_rides), default=0)
    for ride in sorted(open_rides, key=lambda r: r.wait_time, reverse=True):
        bar_length = round((ride.wait_time / max_wait) * MAX_BAR_LENGTH) if max_wait else 0
        bar = "#" * bar_length
        print(f"{ride.wait_time:>4} min  {bar:<{MAX_BAR_LENGTH}}  {ride.name}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="disney_park_info", description="Look up Disney park attraction wait times."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List supported parks by country")

    status_parser = subparsers.add_parser("status", help="Show current wait times for a park")
    status_parser.add_argument("park_key", help="Park key, e.g. tokyo-disneyland (see 'list')")

    args = parser.parse_args(argv)

    if args.command == "list":
        _print_park_list()
        return 0

    return _print_park_status(args.park_key)


if __name__ == "__main__":
    sys.exit(main())
