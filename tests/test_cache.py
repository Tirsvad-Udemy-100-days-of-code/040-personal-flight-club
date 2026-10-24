from unittest.mock import MagicMock, patch

import requests_cache

from flight_club.cache import install_flight_cache
from flight_club.constants import CACHE_EXPIRE_SECONDS, CACHE_NAME, SHEETY_HOST


def test_install_flight_cache_never_caches_sheety() -> None:
    with patch("flight_club.cache.requests_cache.install_cache", new=MagicMock()) as install:
        install_flight_cache()
    install.assert_called_once_with(
        CACHE_NAME,
        expire_after=CACHE_EXPIRE_SECONDS,
        urls_expire_after={f"{SHEETY_HOST}*": requests_cache.DO_NOT_CACHE},
    )
