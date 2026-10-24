from datetime import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
import requests

from flight_club.constants import (
    CURRENCY,
    DEFAULT_MOCK_FLIGHTS_URL,
    REQUEST_TIMEOUT_SECONDS,
    SERPAPI_URL,
)
from flight_club.flight_search import FlightSearch, FlightSearchError

API_KEY = "serp-secret-key"
APP_ID = "mock-app-id-value"
APP_KEY = "mock-app-key-secret"
FROM_TIME = datetime(2026, 6, 15)
TO_TIME = datetime(2026, 6, 22)
BODY: dict[str, Any] = {"best_flights": [{"flights": [], "price": 99}]}


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "FLIGHT_PROVIDER",
        "SERPAPI_API_KEY",
        "MOCK_FLIGHTS_APP_ID",
        "MOCK_FLIGHTS_APP_KEY",
        "MOCK_FLIGHTS_URL",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("SERPAPI_API_KEY", API_KEY)


def _use_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FLIGHT_PROVIDER", "mock")
    monkeypatch.setenv("MOCK_FLIGHTS_APP_ID", APP_ID)
    monkeypatch.setenv("MOCK_FLIGHTS_APP_KEY", APP_KEY)


def _session(status: int = 200, body: Any = BODY, invalid_json: bool = False) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    if invalid_json:
        response.json.side_effect = ValueError("bad json")
    else:
        response.json.return_value = body
    session = MagicMock()
    session.get.return_value = response
    return session


def _search(session: MagicMock) -> dict[str, Any] | None:
    return FlightSearch(session).check_flights("LHR", "CDG", FROM_TIME, TO_TIME)


def test_check_flights_sends_serpapi_params() -> None:
    session = _session()
    assert _search(session) == BODY
    args, kwargs = session.get.call_args
    assert args == (SERPAPI_URL,)
    assert kwargs["params"] == {
        "engine": "google_flights",
        "departure_id": "LHR",
        "arrival_id": "CDG",
        "outbound_date": "2026-06-15",
        "return_date": "2026-06-22",
        "type": "1",
        "adults": "1",
        "currency": CURRENCY,
        "api_key": API_KEY,
    }
    assert kwargs["timeout"] == REQUEST_TIMEOUT_SECONDS


def test_check_flights_uses_mock_headers_and_default_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _use_mock(monkeypatch)
    session = _session()
    assert _search(session) == BODY
    args, kwargs = session.get.call_args
    assert args == (DEFAULT_MOCK_FLIGHTS_URL,)
    assert kwargs["headers"] == {"x-app-id": APP_ID, "x-app-key": APP_KEY}
    assert kwargs["params"]["api_key"] == APP_KEY
    assert kwargs["params"]["departure_id"] == "LHR"


def test_default_mock_url_targets_flights_search_when_env_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert DEFAULT_MOCK_FLIGHTS_URL.endswith("/v1/flights/search")
    _use_mock(monkeypatch)
    session = _session()
    _search(session)
    assert session.get.call_args.args[0].endswith("/v1/flights/search")


def test_check_flights_uses_mock_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _use_mock(monkeypatch)
    monkeypatch.setenv("MOCK_FLIGHTS_URL", "https://example.test/flights")
    session = _session()
    _search(session)
    assert session.get.call_args.args == ("https://example.test/flights",)


def test_init_raises_for_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FLIGHT_PROVIDER", "carrier-pigeon")
    with pytest.raises(FlightSearchError, match="FLIGHT_PROVIDER"):
        FlightSearch()


def test_init_raises_without_serpapi_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SERPAPI_API_KEY")
    with pytest.raises(FlightSearchError, match="SERPAPI_API_KEY"):
        FlightSearch()


@pytest.mark.parametrize("missing", ["MOCK_FLIGHTS_APP_ID", "MOCK_FLIGHTS_APP_KEY"])
def test_init_raises_without_mock_credentials(
    monkeypatch: pytest.MonkeyPatch, missing: str
) -> None:
    _use_mock(monkeypatch)
    monkeypatch.delenv(missing)
    with pytest.raises(FlightSearchError, match=missing):
        FlightSearch()


def test_check_flights_returns_none_on_http_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _search(_session(status=500)) is None
    assert "500" in capsys.readouterr().out


def test_check_flights_prints_service_error_text_on_http_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _use_mock(monkeypatch)
    text = "Invalid input: expected string, received undefined"
    assert _search(_session(status=400, body={"error": text})) is None
    captured = capsys.readouterr()
    assert f"Flight search failed with HTTP 400: {text}." in captured.out
    for secret in (API_KEY, APP_ID, APP_KEY):
        assert secret not in captured.out + captured.err


def test_check_flights_truncates_long_service_error_text(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _search(_session(status=400, body={"error": "x" * 500})) is None
    out = capsys.readouterr().out
    assert "x" * 200 in out
    assert "x" * 201 not in out


@pytest.mark.parametrize("body", [["error"], {"error": 5}, {"other": "x"}])
def test_check_flights_falls_back_when_error_body_is_not_text(
    capsys: pytest.CaptureFixture[str], body: Any
) -> None:
    assert _search(_session(status=500, body=body)) is None
    assert capsys.readouterr().out == "Flight search failed with HTTP 500.\n"


def test_check_flights_falls_back_when_error_body_is_not_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _search(_session(status=502, invalid_json=True)) is None
    assert capsys.readouterr().out == "Flight search failed with HTTP 502.\n"


def test_check_flights_returns_none_on_invalid_json(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _search(_session(invalid_json=True)) is None
    assert "invalid JSON" in capsys.readouterr().out


def test_check_flights_returns_none_on_error_body(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert _search(_session(body={"error": "Invalid API key"})) is None
    assert "Invalid API key" in capsys.readouterr().out


def test_check_flights_returns_none_on_connection_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    session = MagicMock()
    session.get.side_effect = requests.ConnectionError(f"failed for key {API_KEY}")
    assert _search(session) is None
    assert "ConnectionError" in capsys.readouterr().out


def test_check_flights_never_prints_serpapi_key(
    capsys: pytest.CaptureFixture[str],
) -> None:
    session = MagicMock()
    session.get.side_effect = requests.ConnectionError(f"failed for key {API_KEY}")
    _search(session)
    _search(_session(status=500))
    _search(_session(body={"error": "bad"}))
    captured = capsys.readouterr()
    assert API_KEY not in captured.out + captured.err


def test_check_flights_never_prints_mock_secrets(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _use_mock(monkeypatch)
    session = MagicMock()
    session.get.side_effect = requests.ConnectionError(f"{APP_ID} {APP_KEY}")
    _search(session)
    _search(_session(status=500))
    captured = capsys.readouterr()
    assert APP_ID not in captured.out + captured.err
    assert APP_KEY not in captured.out + captured.err
