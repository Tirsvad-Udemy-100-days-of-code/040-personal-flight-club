"""
@file
@brief Picks the cheapest flight out of a SerpApi Google Flights response.
"""

from dataclasses import dataclass
from typing import Any

from flight_club.constants import NOT_AVAILABLE


## @brief The cheapest flight found for one destination; `stops` is the number of stopovers.
@dataclass
class FlightData:
    price: float | int | str
    origin_airport: str
    destination_airport: str
    out_date: str
    return_date: str
    stops: int = 0


def _unavailable() -> FlightData:
    return FlightData(
        price=NOT_AVAILABLE,
        origin_airport=NOT_AVAILABLE,
        destination_airport=NOT_AVAILABLE,
        out_date=NOT_AVAILABLE,
        return_date=NOT_AVAILABLE,
    )


def _parse_price(entry: dict[str, Any]) -> float | None:
    price = entry.get("price")
    if isinstance(price, bool):
        return None
    try:
        return float(price)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _build_flight(entry: dict[str, Any], price: float, return_date: str) -> FlightData | None:
    try:
        legs = entry["flights"]
        return FlightData(
            price=price,
            origin_airport=legs[0]["departure_airport"]["id"],
            destination_airport=legs[-1]["arrival_airport"]["id"],
            out_date=legs[0]["departure_airport"]["time"].split(" ")[0],
            return_date=return_date,
            stops=len(legs) - 1,
        )
    except (KeyError, IndexError, TypeError, AttributeError):
        return None


## @brief Finds the lowest priced flight across best and other flights.
#  @param data SerpApi response, or None when the search failed.
#  @param return_date Return date to store on the result.
#  @return The cheapest flight, or a FlightData filled with "N/A" when none is usable.
def find_cheapest_flight(data: dict[str, Any] | None, return_date: str) -> FlightData:
    if not data:
        print("No flight data available.")
        return _unavailable()

    entries = [*data.get("best_flights", []), *data.get("other_flights", [])]
    cheapest: FlightData | None = None
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        price = _parse_price(entry)
        if price is None:
            continue
        if cheapest is not None and price >= float(cheapest.price):
            continue
        flight = _build_flight(entry, price, return_date)
        if flight is not None:
            cheapest = flight

    if cheapest is None:
        print("No valid flight found in the response.")
        return _unavailable()
    return cheapest
