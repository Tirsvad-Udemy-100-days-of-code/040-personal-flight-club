from typing import Any

import pytest

from flight_club.constants import NOT_AVAILABLE
from flight_club.flight_data import FlightData, find_cheapest_flight

RETURN_DATE = "2026-06-22"

SAMPLE_RESPONSE: dict[str, Any] = {
    "best_flights": [
        {
            "flights": [
                {
                    "departure_airport": {"id": "LHR", "time": "2026-06-15 10:30"},
                    "arrival_airport": {"id": "CDG", "time": "2026-06-15 12:50"},
                }
            ],
            "price": 120,
        }
    ],
    "other_flights": [
        {
            "flights": [
                {
                    "departure_airport": {"id": "LHR", "time": "2026-06-16 07:00"},
                    "arrival_airport": {"id": "CDG", "time": "2026-06-16 09:20"},
                }
            ],
            "price": 95,
        },
        {
            "flights": [
                {
                    "departure_airport": {"id": "LHR", "time": "2026-06-17 18:00"},
                    "arrival_airport": {"id": "CDG", "time": "2026-06-17 20:20"},
                }
            ],
            "price": 210,
        },
    ],
}


def _entry(price: Any, origin: str = "LHR", destination: str = "CDG") -> dict[str, Any]:
    return {
        "flights": [
            {
                "departure_airport": {"id": origin, "time": "2026-07-01 08:00"},
                "arrival_airport": {"id": destination, "time": "2026-07-01 10:00"},
            }
        ],
        "price": price,
    }


def _unavailable() -> FlightData:
    return FlightData(NOT_AVAILABLE, NOT_AVAILABLE, NOT_AVAILABLE, NOT_AVAILABLE, NOT_AVAILABLE)


def test_find_cheapest_flight_picks_lowest_across_both_lists() -> None:
    result = find_cheapest_flight(SAMPLE_RESPONSE, RETURN_DATE)
    assert result == FlightData(95, "LHR", "CDG", "2026-06-16", RETURN_DATE)


def test_find_cheapest_flight_uses_only_other_flights_when_best_missing() -> None:
    data = {"other_flights": [_entry(80), _entry(60, destination="ORY")]}
    result = find_cheapest_flight(data, RETURN_DATE)
    assert result.price == 60
    assert result.destination_airport == "ORY"


def test_find_cheapest_flight_skips_missing_price() -> None:
    data = {"best_flights": [{"flights": _entry(1)["flights"]}, _entry(150)]}
    assert find_cheapest_flight(data, RETURN_DATE).price == 150


@pytest.mark.parametrize("price", ["abc", None, [], True])
def test_find_cheapest_flight_skips_non_numeric_price(price: Any) -> None:
    data = {"best_flights": [_entry(price), _entry(300)]}
    assert find_cheapest_flight(data, RETURN_DATE).price == 300


def test_find_cheapest_flight_returns_unavailable_for_empty_dict() -> None:
    assert find_cheapest_flight({}, RETURN_DATE) == _unavailable()


def test_find_cheapest_flight_returns_unavailable_for_none(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert find_cheapest_flight(None, RETURN_DATE) == _unavailable()
    assert capsys.readouterr().out.strip() != ""


def test_find_cheapest_flight_skips_malformed_entries() -> None:
    data = {
        "best_flights": [
            {"price": 10},
            {"flights": [], "price": 10},
            {"flights": [{"departure_airport": {}}], "price": 10},
            "not a dict",
            _entry(200),
        ]
    }
    assert find_cheapest_flight(data, RETURN_DATE).price == 200


def test_find_cheapest_flight_returns_unavailable_when_all_malformed() -> None:
    data = {"best_flights": [{"price": 10}, {"flights": [], "price": 5}]}
    assert find_cheapest_flight(data, RETURN_DATE) == _unavailable()


def test_find_cheapest_flight_takes_destination_from_last_leg() -> None:
    entry = {
        "flights": [
            {
                "departure_airport": {"id": "LHR", "time": "2026-08-01 06:00"},
                "arrival_airport": {"id": "AMS", "time": "2026-08-01 08:00"},
            },
            {
                "departure_airport": {"id": "AMS", "time": "2026-08-01 09:30"},
                "arrival_airport": {"id": "BCN", "time": "2026-08-01 11:45"},
            },
        ],
        "price": 140,
    }
    result = find_cheapest_flight({"best_flights": [entry]}, RETURN_DATE)
    assert result.origin_airport == "LHR"
    assert result.destination_airport == "BCN"


def test_find_cheapest_flight_trims_time_from_out_date() -> None:
    result = find_cheapest_flight({"best_flights": [_entry(50)]}, RETURN_DATE)
    assert result.out_date == "2026-07-01"
    assert result.return_date == RETURN_DATE


def _multi_leg_entry(price: float, legs: int) -> dict[str, Any]:
    segment = {
        "departure_airport": {"id": "LHR", "time": "2026-07-01 08:00"},
        "arrival_airport": {"id": "DPS", "time": "2026-07-02 10:00"},
    }
    return {"flights": [segment] * legs, "price": price}


@pytest.mark.parametrize(("legs", "stops"), [(1, 0), (2, 1), (3, 2)])
def test_stops_is_the_number_of_segments_minus_one(legs: int, stops: int) -> None:
    cheapest = find_cheapest_flight({"best_flights": [_multi_leg_entry(500, legs)]}, RETURN_DATE)
    assert cheapest.stops == stops


def test_unavailable_flight_has_no_stops() -> None:
    assert find_cheapest_flight(None, RETURN_DATE).stops == 0
