# disney-park-info

A small CLI and web tool for checking current attraction wait times and
congestion across Disney parks worldwide, using the free public
[queue-times.com](https://queue-times.com) API.

## Supported parks

- Tokyo Disneyland / Tokyo DisneySea (Japan)
- Disneyland / Disney California Adventure (United States, Anaheim)
- Disney Magic Kingdom / Disney Hollywood Studios / Animal Kingdom (United States, Orlando)
- Disneyland Park Paris / Disney Adventure World Paris (France)
- Disneyland Hong Kong (Hong Kong)
- Shanghai Disney Resort (China)

Run `python -m disney_park_info list` for the full list with keys.

## Install

```
pip install -r requirements.txt
```

## Usage

List supported parks:

```
python -m disney_park_info list
```

Show current wait times and congestion for a park:

```
python -m disney_park_info status tokyo-disneyland
```

Output is sorted by wait time (longest first) with a text bar showing
relative congestion, plus a summary of open/closed attraction counts and
the average wait time.

### Web UI

Start a local web server:

```
python -m disney_park_info serve
```

Then open http://127.0.0.1:5000 in a browser, pick a park from the
dropdown, and see the same wait-time data as a sorted bar chart.

## Tests

```
python -m pytest tests/
```

## Scope

This tool only reads publicly available wait-time data. It does not
scrape official Disney sites and does not perform any booking, ticketing,
or purchasing actions. Parade and show schedules are not currently
available through the queue-times.com API and are out of scope for now.
