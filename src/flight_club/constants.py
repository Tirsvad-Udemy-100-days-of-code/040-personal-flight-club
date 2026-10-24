"""
@file
@brief Constants shared across Flight Club. Holds no logic.
"""

## @brief IATA code of the airport every search departs from.
ORIGIN_AIRPORT = "LHR"

## @brief Currency of every price requested and shown.
CURRENCY = "GBP"

## @brief SerpApi search endpoint.
SERPAPI_URL = "https://serpapi.com/search"

## @brief SerpApi engine used for flight searches.
SERPAPI_ENGINE = "google_flights"

## @brief Default URL of the course's mock flight service (overridable via the MOCK_FLIGHTS_URL environment variable).
DEFAULT_MOCK_FLIGHTS_URL = "https://app.100daysofpython.dev/v1/flights/search"

## @brief Host of the Sheety API.
SHEETY_HOST = "api.sheety.co"

## @brief Name of the local HTTP cache for flight searches.
CACHE_NAME = "flight_cache"

## @brief Seconds a cached flight search stays valid.
CACHE_EXPIRE_SECONDS = 3600

## @brief Length of the search window in days (about six months).
SEARCH_WINDOW_DAYS = 182

## @brief Text shown when no price is available.
NOT_AVAILABLE = "N/A"

## @brief strftime format of dates sent to and read from providers.
DATE_FORMAT = "%Y-%m-%d"

## @brief Name of the SerpApi flight provider.
PROVIDER_SERPAPI = "serpapi"

## @brief Name of the mock flight provider.
PROVIDER_MOCK = "mock"

## @brief Environment variable: Sheety sheet endpoint.
ENV_SHEETY_ENDPOINT = "SHEETY_ENDPOINT"

## @brief Environment variable: Sheety Bearer token.
ENV_SHEETY_TOKEN = "SHEETY_TOKEN"

## @brief Environment variable: selected flight provider.
ENV_FLIGHT_PROVIDER = "FLIGHT_PROVIDER"

## @brief Environment variable: SerpApi API key.
ENV_SERPAPI_API_KEY = "SERPAPI_API_KEY"

## @brief Environment variable: mock flight service app id.
ENV_MOCK_APP_ID = "MOCK_FLIGHTS_APP_ID"

## @brief Environment variable: mock flight service app key.
ENV_MOCK_APP_KEY = "MOCK_FLIGHTS_APP_KEY"

## @brief Environment variable: optional URL of the mock flight service.
ENV_MOCK_FLIGHTS_URL = "MOCK_FLIGHTS_URL"

## @brief Environment variable: WhatsApp recipient number with country code.
ENV_WHATSAPP_NUMBER = "WHATSAPP_NUMBER"

## @brief Seconds pywhatkit waits for WhatsApp Web to load before it sends the message.
WHATSAPP_WAIT_SECONDS = 15

## @brief Seconds pywhatkit waits after sending before it closes the browser tab.
WHATSAPP_CLOSE_SECONDS = 3

## @brief Seconds to wait for an HTTP response before giving up.
REQUEST_TIMEOUT_SECONDS = 30

## @brief The longest piece of the flight service's error text that is printed.
ERROR_TEXT_MAX_LENGTH = 200
