"""
@file
@brief Searches flight prices through SerpApi or the course's mock flight service.
"""

import os
from datetime import datetime
from typing import Any

import requests

from flight_club.constants import (
    CURRENCY,
    DATE_FORMAT,
    DEFAULT_MOCK_FLIGHTS_URL,
    ENV_FLIGHT_PROVIDER,
    ENV_MOCK_APP_ID,
    ENV_MOCK_APP_KEY,
    ENV_MOCK_FLIGHTS_URL,
    ENV_SERPAPI_API_KEY,
    ERROR_TEXT_MAX_LENGTH,
    PROVIDER_MOCK,
    PROVIDER_SERPAPI,
    REQUEST_TIMEOUT_SECONDS,
    SERPAPI_ENGINE,
    SERPAPI_URL,
    STOPS_NONSTOP,
    STOPS_UP_TO_TWO,
)


## @brief Raised when the flight provider is configured wrongly.
class FlightSearchError(RuntimeError):
    pass


## @brief Searches round trip flights with the provider chosen by FLIGHT_PROVIDER.
#
#  The mock provider returns JSON shaped like a SerpApi Google Flights response, with
#  the keys best_flights and other_flights, so both providers feed the same parser.
#  The mock provider is called with the x-app-id and x-app-key headers and also with
#  the app key as the api_key query parameter, which the service requires.
class FlightSearch:
    ## @brief Reads the provider and its credentials from the environment.
    #  @param session Optional HTTP session; a new one is made per call if omitted.
    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session
        self._provider = os.environ.get(ENV_FLIGHT_PROVIDER) or PROVIDER_SERPAPI
        self._api_key: str | None = None
        self._url = SERPAPI_URL
        self._headers: dict[str, str] = {}
        if self._provider == PROVIDER_SERPAPI:
            self._api_key = self._require_env(ENV_SERPAPI_API_KEY)
        elif self._provider == PROVIDER_MOCK:
            app_key = self._require_env(ENV_MOCK_APP_KEY)
            self._headers = {
                "x-app-id": self._require_env(ENV_MOCK_APP_ID),
                "x-app-key": app_key,
            }
            # The real mock service also demands the app key as the api_key query parameter.
            self._api_key = app_key
            self._url = os.environ.get(ENV_MOCK_FLIGHTS_URL) or DEFAULT_MOCK_FLIGHTS_URL
        else:
            raise FlightSearchError(
                f"Unknown {ENV_FLIGHT_PROVIDER} '{self._provider}'; "
                f"use '{PROVIDER_SERPAPI}' or '{PROVIDER_MOCK}'."
            )

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.environ.get(name)
        if not value:
            raise FlightSearchError(f"Environment variable {name} is not set.")
        return value

    ## @brief Reads the service's own error text from a failed response.
    #  @return The "error" string of a JSON body cut to the limit, or None if there is none.
    @staticmethod
    def _service_error_text(response: requests.Response) -> str | None:
        try:
            body = response.json()
        except ValueError:
            return None
        if isinstance(body, dict) and isinstance(body.get("error"), str):
            return str(body["error"])[:ERROR_TEXT_MAX_LENGTH]
        return None

    def _get_session(self) -> requests.Session:
        # Created at call time so requests_cache.install_cache patching applies.
        return self._session if self._session is not None else requests.Session()

    def _build_params(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: datetime,
        to_time: datetime,
        is_direct: bool,
    ) -> dict[str, str]:
        params = {
            "engine": SERPAPI_ENGINE,
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime(DATE_FORMAT),
            "return_date": to_time.strftime(DATE_FORMAT),
            "type": "1",
            "adults": "1",
            "currency": CURRENCY,
            "stops": STOPS_NONSTOP if is_direct else STOPS_UP_TO_TWO,
        }
        if self._api_key is not None:
            params["api_key"] = self._api_key
        return params

    ## @brief Searches the cheapest round trips between two airports.
    #  @param origin_city_code IATA code to depart from.
    #  @param destination_city_code IATA code to arrive at.
    #  @param from_time Outbound date.
    #  @param to_time Return date.
    #  @param is_direct True for nonstop flights only, False to allow up to two stops.
    #  @return The decoded response, or None after printing why the search failed.
    def check_flights(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: datetime,
        to_time: datetime,
        is_direct: bool = True,
    ) -> dict[str, Any] | None:
        params = self._build_params(
            origin_city_code, destination_city_code, from_time, to_time, is_direct
        )
        try:
            response = self._get_session().get(
                self._url,
                params=params,
                headers=self._headers or None,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            # The exception type is printed, not its text, which may echo the URL and key.
            print(f"Flight search request failed: {type(error).__name__}.")
            return None
        if not 200 <= response.status_code < 300:
            detail = self._service_error_text(response)
            suffix = f": {detail}" if detail else ""
            print(f"Flight search failed with HTTP {response.status_code}{suffix}.")
            return None
        try:
            body = response.json()
        except ValueError:
            print("Flight search returned invalid JSON.")
            return None
        if not isinstance(body, dict):
            print("Flight search returned an unexpected response shape.")
            return None
        if "error" in body:
            print(f"Flight search returned an error: {body['error']}")
            return None
        return body
