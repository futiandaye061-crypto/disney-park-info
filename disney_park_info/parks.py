"""Registry of Disney parks tracked by this tool.

Park IDs correspond to the public queue-times.com park catalog
(https://queue-times.com/parks.json).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Park:
    key: str
    name: str
    country: str
    queue_times_id: int


PARKS: tuple[Park, ...] = (
    Park("tokyo-disneyland", "Tokyo Disneyland", "Japan", 274),
    Park("tokyo-disneysea", "Tokyo DisneySea", "Japan", 275),
    Park("disneyland-anaheim", "Disneyland", "United States", 16),
    Park("disney-california-adventure", "Disney California Adventure", "United States", 17),
    Park("magic-kingdom", "Disney Magic Kingdom", "United States", 6),
    Park("hollywood-studios", "Disney Hollywood Studios", "United States", 7),
    Park("animal-kingdom", "Animal Kingdom", "United States", 8),
    Park("disneyland-paris", "Disneyland Park Paris", "France", 4),
    Park("disney-adventure-world-paris", "Disney Adventure World Paris", "France", 28),
    Park("disneyland-hong-kong", "Disneyland Hong Kong", "Hong Kong", 31),
    Park("shanghai-disney-resort", "Shanghai Disney Resort", "China", 30),
)

PARKS_BY_KEY: dict[str, Park] = {park.key: park for park in PARKS}


def get_park(key: str) -> Park:
    """Look up a tracked park by its short key.

    Raises KeyError with a message listing valid keys if not found.
    """
    try:
        return PARKS_BY_KEY[key]
    except KeyError:
        valid = ", ".join(sorted(PARKS_BY_KEY))
        raise KeyError(f"Unknown park '{key}'. Valid park keys: {valid}") from None
