from datetime import datetime, timedelta
from typing import Any

import pytest

from flight_club import main as main_module
from flight_club.data_manager import DataManagerError
from flight_club.flight_data import FlightData
from flight_club.main import run

TODAY = datetime(2026, 10, 24, 12, 0)


class FakeDataManager:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.updates: list[tuple[int, float]] = []

    def get_destination_data(self) -> list[dict[str, Any]]:
        return self.rows

    def update_lowest_price(self, row_id: int, new_price: float) -> None:
        self.updates.append((row_id, new_price))


class FakeFlightSearch:
    def __init__(self, price: float | None) -> None:
        self.price = price
        self.calls: list[tuple[str, str, datetime, datetime]] = []

    def check_flights(
        self, origin: str, destination: str, from_time: datetime, to_time: datetime
    ) -> dict[str, Any] | None:
        self.calls.append((origin, destination, from_time, to_time))
        if self.price is None:
            return None
        leg = {
            "departure_airport": {"id": origin, "time": "2026-10-25 08:00"},
            "arrival_airport": {"id": destination, "time": "2026-10-25 10:00"},
        }
        return {"best_flights": [{"price": self.price, "flights": [leg]}]}


class FakeNotificationManager:
    def __init__(self) -> None:
        self.sent: list[str] = []

    def build_message(self, flight: FlightData) -> str:
        return f"alert {flight.destination_airport} {flight.price}"

    def send_whatsapp(self, message: str) -> bool:
        self.sent.append(message)
        return True


def _run(
    rows: list[dict[str, Any]], price: float | None
) -> tuple[list[FlightData], FakeDataManager, FakeFlightSearch, FakeNotificationManager]:
    data, search, notifier = (
        FakeDataManager(rows),
        FakeFlightSearch(price),
        FakeNotificationManager(),
    )
    found = run(data, search, notifier, today=TODAY)  # type: ignore[arg-type]
    return found, data, search, notifier


def _row(lowest: Any = 100) -> dict[str, Any]:
    return {"city": "Paris", "iataCode": "CDG", "lowestPrice": lowest, "id": 2}


def test_run_updates_and_notifies_when_price_is_lower() -> None:
    found, data, _, notifier = _run([_row(100)], 54)
    assert [f.price for f in found] == [54]
    assert data.updates == [(2, 54)]
    assert notifier.sent == ["alert CDG 54.0"]
    assert found[0].return_date == (TODAY + timedelta(days=182)).strftime("%Y-%m-%d")


@pytest.mark.parametrize("price", [100, 150])
def test_run_does_nothing_when_price_is_not_lower(price: float) -> None:
    found, data, _, notifier = _run([_row(100)], price)
    assert found == []
    assert data.updates == []
    assert notifier.sent == []


def test_run_does_nothing_when_price_not_available() -> None:
    found, data, _, notifier = _run([_row(100)], None)
    assert found == []
    assert data.updates == []
    assert notifier.sent == []


@pytest.mark.parametrize("lowest", [None, "", "cheap"])
def test_run_skips_row_without_numeric_lowest_price(lowest: Any) -> None:
    _, data, search, notifier = _run([_row(lowest)], 1)
    assert search.calls == []
    assert data.updates == []
    assert notifier.sent == []


def test_run_skips_row_without_iata_code() -> None:
    row = {"city": "Nowhere", "iataCode": "", "lowestPrice": 100, "id": 3}
    _, _, search, _ = _run([row], 1)
    assert search.calls == []


def test_run_checks_every_row_with_origin_and_dates() -> None:
    rows = [{**_row(), "iataCode": code, "id": i} for i, code in enumerate(["CDG", "BER", "TYO"])]
    _, _, search, _ = _run(rows, None)
    assert [c[:2] for c in search.calls] == [("LHR", "CDG"), ("LHR", "BER"), ("LHR", "TYO")]
    for call in search.calls:
        assert call[2] == TODAY + timedelta(days=1)
        assert call[3] == TODAY + timedelta(days=182)


def test_main_exits_with_one_on_data_manager_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail() -> None:
        raise DataManagerError("Environment variable SHEETY_ENDPOINT is not set.")

    monkeypatch.setattr(main_module, "load_dotenv", lambda: True)
    monkeypatch.setattr(main_module, "install_flight_cache", lambda: None)
    monkeypatch.setattr(main_module, "DataManager", fail)
    with pytest.raises(SystemExit) as exit_info:
        main_module.main()
    assert exit_info.value.code == 1
    assert "SHEETY_ENDPOINT" in capsys.readouterr().out
