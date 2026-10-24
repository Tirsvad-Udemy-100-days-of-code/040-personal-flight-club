"""
@file
@brief Reads and updates the destination sheet through the Sheety API.
"""

import os
import re
from typing import Any

import requests

from flight_club.constants import (
    EMAIL_FIELD,
    EMAIL_PATTERN,
    ENV_SHEETY_ENDPOINT,
    ENV_SHEETY_PRICES_ENDPOINT,
    ENV_SHEETY_TOKEN,
    ENV_SHEETY_USERS_ENDPOINT,
    PRICES_KEY,
    REQUEST_TIMEOUT_SECONDS,
    USERS_KEY,
)


## @brief Raised when the sheet cannot be configured, read or updated.
class DataManagerError(RuntimeError):
    pass


## @brief Talks to the Sheety sheets: the destinations ("prices") and the customers ("users").
class DataManager:
    ## @brief Reads every setting from the environment, in this one place.
    #
    #  The prices endpoint comes from SHEETY_PRICES_ENDPOINT, or from the Day 39 name
    #  SHEETY_ENDPOINT. The users endpoint is optional here and checked when it is used,
    #  so a run without customers still works.
    #  @param session Optional HTTP session; a new one is made per call if omitted.
    def __init__(self, session: requests.Session | None = None) -> None:
        self._prices_endpoint = self._prices_endpoint_from_env()
        self._users_endpoint = os.environ.get(ENV_SHEETY_USERS_ENDPOINT) or None
        self._headers = {"Authorization": f"Bearer {self._require_env(ENV_SHEETY_TOKEN)}"}
        self._session = session

    @classmethod
    def _prices_endpoint_from_env(cls) -> str:
        legacy = os.environ.get(ENV_SHEETY_ENDPOINT)
        if legacy and not os.environ.get(ENV_SHEETY_PRICES_ENDPOINT):
            return legacy
        return cls._require_env(ENV_SHEETY_PRICES_ENDPOINT)

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

    def _read_rows(self, endpoint: str, key: str) -> list[dict[str, Any]]:
        response = self._get_session().get(
            endpoint, headers=self._headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        self._check(response, "read")
        body = response.json()
        rows = body.get(key) if isinstance(body, dict) else None
        if not isinstance(rows, list):
            raise DataManagerError(f"Sheety response has no '{key}' list.")
        return rows

    ## @brief Fetch every destination row from the Google Sheet through the Sheety API.
    #  @return Rows such as {'city': 'Paris', 'iataCode': 'CDG', 'lowestPrice': 54, 'id': 2}.
    def get_destination_data(self) -> list[dict[str, Any]]:
        return self._read_rows(self._prices_endpoint, PRICES_KEY)

    ## @brief Fetch every customer row from the "users" sheet.
    #  @return Rows such as {'firstName': 'Ann', 'email': 'ann@example.com', 'id': 2}.
    def get_customer_emails(self) -> list[dict[str, Any]]:
        if self._users_endpoint is None:
            raise DataManagerError(f"Environment variable {ENV_SHEETY_USERS_ENDPOINT} is not set.")
        return self._read_rows(self._users_endpoint, USERS_KEY)

    ## @brief Picks the usable email addresses out of the customer rows.
    #  @param customers Rows from get_customer_emails().
    #  @return The addresses that look like an email address, in sheet order, without duplicates.
    @staticmethod
    def extract_emails(customers: list[dict[str, Any]]) -> list[str]:
        emails: list[str] = []
        for customer in customers:
            email = customer.get(EMAIL_FIELD)
            if not isinstance(email, str):
                continue
            email = email.strip()
            if re.fullmatch(EMAIL_PATTERN, email) and email not in emails:
                emails.append(email)
        return emails

    ## @brief Stores a new lowest price for one row.
    #  @param row_id Sheety row id.
    #  @param new_price The new lowest price.
    #  @return None
    def update_lowest_price(self, row_id: int, new_price: float) -> None:
        response = self._get_session().put(
            f"{self._prices_endpoint}/{row_id}",
            json={"price": {"lowestPrice": new_price}},
            headers=self._headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        self._check(response, "update")
