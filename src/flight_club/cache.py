"""
@file
@brief Local HTTP cache for flight searches.
"""

import requests_cache

from flight_club.constants import CACHE_EXPIRE_SECONDS, CACHE_NAME, SHEETY_HOST


## @brief Installs the HTTP cache; Sheety traffic is never cached.
#  @return None
def install_flight_cache() -> None:
    requests_cache.install_cache(
        CACHE_NAME,
        expire_after=CACHE_EXPIRE_SECONDS,
        urls_expire_after={f"{SHEETY_HOST}*": requests_cache.DO_NOT_CACHE},
    )
