"""Web UI for disney-park-info.

Serves a single page that lets visitors pick a park and see current
attraction wait times as a sorted chart, backed by a small JSON API.
"""

from flask import Flask, jsonify, render_template

from disney_park_info.api import get_ride_wait_times
from disney_park_info.parks import PARKS, get_park

app = Flask(__name__)


@app.get("/")
def index():
    parks = sorted(PARKS, key=lambda p: (p.country, p.name))
    return render_template("index.html", parks=parks)


@app.get("/api/status/<park_key>")
def park_status(park_key):
    try:
        park = get_park(park_key)
    except KeyError as exc:
        return jsonify({"error": str(exc)}), 404

    rides = get_ride_wait_times(park.queue_times_id)
    open_rides = [ride for ride in rides if ride.is_open]
    average_wait = sum(ride.wait_time for ride in open_rides) / len(open_rides) if open_rides else 0

    return jsonify(
        {
            "park": {"key": park.key, "name": park.name, "country": park.country},
            "open_count": len(open_rides),
            "closed_count": len(rides) - len(open_rides),
            "average_wait": round(average_wait),
            "rides": [
                {"name": ride.name, "wait_time": ride.wait_time}
                for ride in sorted(open_rides, key=lambda r: r.wait_time, reverse=True)
            ],
        }
    )


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
