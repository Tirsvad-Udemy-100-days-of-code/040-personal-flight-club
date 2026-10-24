from datetime import date

from flight_club import constants


def test_search_window_is_positive() -> None:
    assert constants.SEARCH_WINDOW_DAYS > 0


def test_provider_names_are_distinct() -> None:
    assert constants.PROVIDER_SERPAPI != constants.PROVIDER_MOCK


def test_origin_is_three_letter_code() -> None:
    assert len(constants.ORIGIN_AIRPORT) == 3
    assert constants.ORIGIN_AIRPORT.isalpha()
    assert constants.ORIGIN_AIRPORT.isupper()


def test_urls_use_https() -> None:
    assert constants.SERPAPI_URL.startswith("https://")
    assert constants.DEFAULT_MOCK_FLIGHTS_URL.startswith("https://")


def test_date_format_round_trips() -> None:
    day = date(2026, 1, 31)
    assert day.strftime(constants.DATE_FORMAT) == "2026-01-31"


def test_env_variable_names_are_distinct() -> None:
    names = [value for key, value in vars(constants).items() if key.startswith("ENV_")]
    assert len(names) == len(set(names))
