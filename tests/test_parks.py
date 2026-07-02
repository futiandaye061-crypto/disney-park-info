import pytest

from disney_park_info.parks import PARKS, get_park


def test_park_keys_are_unique():
    keys = [park.key for park in PARKS]
    assert len(keys) == len(set(keys))


def test_park_ids_are_unique():
    ids = [park.queue_times_id for park in PARKS]
    assert len(ids) == len(set(ids))


def test_get_park_returns_known_park():
    park = get_park("tokyo-disneyland")
    assert park.name == "Tokyo Disneyland"
    assert park.country == "Japan"


def test_get_park_raises_for_unknown_key():
    with pytest.raises(KeyError, match="Unknown park 'not-a-park'"):
        get_park("not-a-park")
