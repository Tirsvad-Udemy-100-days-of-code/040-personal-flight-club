"""
@file
@brief Entry point: checks every destination in the sheet and alerts on lower prices.

Run it from the project root with `python -m flight_club` or the `flight-club` command,
after filling the variables described in the README into a local `.env` file.
"""

import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

from flight_club.cache import install_flight_cache
from flight_club.constants import (
    CURRENCY,
    DATE_FORMAT,
    NOT_AVAILABLE,
    ORIGIN_AIRPORT,
    SEARCH_WINDOW_DAYS,
)
from flight_club.data_manager import DataManager, DataManagerError
from flight_club.flight_data import FlightData, find_cheapest_flight
from flight_club.flight_search import FlightSearch, FlightSearchError
from flight_club.notification_manager import NotificationManager


def _is_checkable(row: dict[str, object]) -> bool:
    price = row.get("lowestPrice")
    return (
        bool(row.get("iataCode")) and isinstance(price, int | float) and not isinstance(price, bool)
    )


def _get_customer_emails(data_manager: DataManager) -> list[str]:
    try:
        return data_manager.extract_emails(data_manager.get_customer_emails())
    except DataManagerError as error:
        print(f"No emails sent: {error}")
        return []


## @brief Checks every sheet row and reports each flight cheaper than the stored price.
#  @param data_manager Source of the destination rows and target of price updates.
#  @param flight_search Provider of flight offers.
#  @param notification_manager Sender of the alerts.
#  @param today Start of the run; the current time when omitted.
#  @return The cheaper flights that were found.
def run(
    data_manager: DataManager,
    flight_search: FlightSearch,
    notification_manager: NotificationManager,
    today: datetime | None = None,
) -> list[FlightData]:
    today = today if today is not None else datetime.now()
    tomorrow = today + timedelta(days=1)
    six_month_from_today = today + timedelta(days=SEARCH_WINDOW_DAYS)
    return_date = six_month_from_today.strftime(DATE_FORMAT)
    found: list[FlightData] = []
    customer_emails: list[str] | None = None

    sheet_data = data_manager.get_destination_data()
    for row in sheet_data:
        if not _is_checkable(row):
            print(f"Skipping row without an IATA code or a numeric lowest price: {row.get('city')}")
            continue
        print(f"Getting direct flights for {row['city']}...")
        flights = flight_search.check_flights(
            ORIGIN_AIRPORT, row["iataCode"], tomorrow, six_month_from_today
        )
        cheapest = find_cheapest_flight(flights, return_date)
        if cheapest.price == NOT_AVAILABLE:
            print(f"No direct flight to {row['city']}. Looking for indirect flights...")
            flights = flight_search.check_flights(
                ORIGIN_AIRPORT, row["iataCode"], tomorrow, six_month_from_today, is_direct=False
            )
            cheapest = find_cheapest_flight(flights, return_date)
        print(f"{row['city']}: {CURRENCY} {cheapest.price}")
        if cheapest.price != NOT_AVAILABLE and cheapest.price < row["lowestPrice"]:
            print(f"Lower price flight found to {row['city']}!")
            data_manager.update_lowest_price(row["id"], cheapest.price)  # type: ignore[arg-type]
            message = notification_manager.build_message(cheapest)
            notification_manager.send_whatsapp(message)
            if customer_emails is None:
                customer_emails = _get_customer_emails(data_manager)
            notification_manager.send_emails(customer_emails, message)
            found.append(cheapest)
    return found


## @brief Wires the real collaborators and runs one check; exits with 1 on a setup error.
#  @return None
def main() -> None:
    load_dotenv()
    install_flight_cache()
    try:
        run(DataManager(), FlightSearch(), NotificationManager())
    except (DataManagerError, FlightSearchError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
