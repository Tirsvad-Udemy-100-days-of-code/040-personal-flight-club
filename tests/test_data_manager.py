from typing import Any
from unittest.mock import MagicMock

import pytest

from flight_club.constants import REQUEST_TIMEOUT_SECONDS
from flight_club.data_manager import DataManager, DataManagerError

ENDPOINT = "https://api.sheety.co/abc/flights/prices"
USERS_ENDPOINT = "https://api.sheety.co/abc/flights/users"
TOKEN = "super-secret-token"


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHEETY_ENDPOINT", raising=False)
    monkeypatch.setenv("SHEETY_PRICES_ENDPOINT", ENDPOINT)
    monkeypatch.setenv("SHEETY_USERS_ENDPOINT", USERS_ENDPOINT)
    monkeypatch.setenv("SHEETY_TOKEN", TOKEN)


def _session(status: int = 200, body: Any = None) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.json.return_value = body
    session = MagicMock()
    session.get.return_value = response
    session.put.return_value = response
    return session


def test_get_destination_data_returns_prices() -> None:
    rows = [{"city": "Paris", "iataCode": "CDG", "lowestPrice": 54, "id": 2}]
    session = _session(body={"prices": rows})
    assert DataManager(session).get_destination_data() == rows
    session.get.assert_called_once_with(
        ENDPOINT,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )


@pytest.mark.parametrize("body", [{}, {"prices": "x"}, [1]])
def test_get_destination_data_raises_without_prices_list(body: Any) -> None:
    with pytest.raises(DataManagerError, match="prices"):
        DataManager(_session(body=body)).get_destination_data()


@pytest.mark.parametrize("status", [500, 401])
def test_get_destination_data_raises_on_http_error(status: int) -> None:
    with pytest.raises(DataManagerError, match=str(status)):
        DataManager(_session(status=status)).get_destination_data()


def test_update_lowest_price_puts_payload() -> None:
    session = _session()
    DataManager(session).update_lowest_price(7, 49.5)
    session.put.assert_called_once_with(
        f"{ENDPOINT}/7",
        json={"price": {"lowestPrice": 49.5}},
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )


@pytest.mark.parametrize("status", [500, 401])
def test_update_lowest_price_raises_on_http_error(status: int) -> None:
    with pytest.raises(DataManagerError, match=str(status)):
        DataManager(_session(status=status)).update_lowest_price(1, 10)


def test_errors_never_contain_token() -> None:
    with pytest.raises(DataManagerError) as read_error:
        DataManager(_session(status=401)).get_destination_data()
    with pytest.raises(DataManagerError) as write_error:
        DataManager(_session(status=500)).update_lowest_price(1, 10)
    assert TOKEN not in str(read_error.value)
    assert TOKEN not in str(write_error.value)


@pytest.mark.parametrize("name", ["SHEETY_PRICES_ENDPOINT", "SHEETY_TOKEN"])
def test_missing_env_variable_names_the_variable(
    monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.delenv(name)
    with pytest.raises(DataManagerError, match=name):
        DataManager(_session())


USERS = [
    {"firstName": "Ann", "lastName": "Lee", "email": "ann@example.com", "id": 2},
    {"firstName": "Bo", "lastName": "Kim", "email": " bo@example.com ", "id": 3},
]


def test_get_customer_emails_returns_users() -> None:
    session = _session(body={"users": USERS})
    assert DataManager(session).get_customer_emails() == USERS
    session.get.assert_called_once_with(
        USERS_ENDPOINT,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )


@pytest.mark.parametrize("body", [{}, {"users": "x"}, [1]])
def test_get_customer_emails_raises_without_users_list(body: Any) -> None:
    with pytest.raises(DataManagerError, match="users"):
        DataManager(_session(body=body)).get_customer_emails()


def test_get_customer_emails_raises_on_http_error() -> None:
    with pytest.raises(DataManagerError, match="401"):
        DataManager(_session(status=401)).get_customer_emails()


def test_get_customer_emails_needs_the_users_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHEETY_USERS_ENDPOINT")
    manager = DataManager(_session(body={"users": USERS}))
    with pytest.raises(DataManagerError, match="SHEETY_USERS_ENDPOINT"):
        manager.get_customer_emails()


def test_extract_emails_keeps_valid_unique_addresses() -> None:
    customers: list[dict[str, Any]] = [
        *USERS,
        {"email": "ann@example.com"},
        {"email": "not-an-email"},
        {"email": None},
        {"firstName": "No", "lastName": "Mail"},
    ]
    assert DataManager.extract_emails(customers) == ["ann@example.com", "bo@example.com"]


def test_legacy_endpoint_name_is_still_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHEETY_PRICES_ENDPOINT")
    monkeypatch.setenv("SHEETY_ENDPOINT", "https://api.sheety.co/old/prices")
    session = _session(body={"prices": []})
    DataManager(session).get_destination_data()
    assert session.get.call_args.args == ("https://api.sheety.co/old/prices",)


def test_prices_endpoint_wins_over_the_legacy_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHEETY_ENDPOINT", "https://api.sheety.co/old/prices")
    session = _session(body={"prices": []})
    DataManager(session).get_destination_data()
    assert session.get.call_args.args == (ENDPOINT,)
