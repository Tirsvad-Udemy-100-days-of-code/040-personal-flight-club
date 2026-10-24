"""
@file
@brief Reads and updates the destination sheet through the Sheety API.
"""

import os
from typing import Any

import requests

from flight_club.constants import (
    ENV_SHEETY_ENDPOINT,
    ENV_SHEETY_TOKEN,
    REQUEST_TIMEOUT_SECONDS,
)


## @brief Raised when the sheet cannot be configured, read or updated.
class DataManagerError(RuntimeError):
    pass


## @brief Talks to the Sheety sheet that holds the destinations.
class DataManager:
    ## @brief Reads the endpoint and token from the environment.
    #  @param session Optional HTTP session; a new one is made per call if omitted.
    def __init__(self, session: requests.Session | None = None) -> None:
        self._endpoint = self._require_env(ENV_SHEETY_ENDPOINT)
        self._headers = {"Authorization": f"Bearer {self._require_env(ENV_SHEETY_TOKEN)}"}
        self._session = session

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.environ.get(name)
        if not value:
            raise DataManagerError(f"Environment variable {name} is not set.")
        return value

    def _get_session(self) -> requests.Session:
        # Created at call time so requests_cache.install_cache patching applies.
        return self._session if self._session is not None else requests.Session()

    @staticmethod
    def _check(response: requests.Response, action: str) -> None:
        if not 200 <= response.status_code < 300:
            raise DataManagerError(f"Sheety {action} failed with HTTP {response.status_code}.")

    ## @brief Fetch every destination row from the Google Sheet through the Sheety API.
    #  @return Rows such as {'city': 'Paris', 'iataCode': 'CDG', 'lowestPrice': 54, 'id': 2}.
    def get_destination_data(self) -> list[dict[str, Any]]:
        response = self._get_session().get(
            self._endpoint, headers=self._headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        self._check(response, "read")
        body = response.json()
        prices = body.get("prices") if isinstance(body, dict) else None
        if not isinstance(prices, list):
            raise DataManagerError("Sheety response has no 'prices' list.")
        return prices

    ## @brief Stores a new lowest price for one row.
    #  @param row_id Sheety row id.
    #  @param new_price The new lowest price.
    #  @return None
    def update_lowest_price(self, row_id: int, new_price: float) -> None:
        response = self._get_session().put(
            f"{self._endpoint}/{row_id}",
            json={"price": {"lowestPrice": new_price}},
            headers=self._headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        self._check(response, "update")
