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

## @brief SerpApi `stops` value that asks for nonstop flights only.
STOPS_NONSTOP = "1"

## @brief SerpApi `stops` value that allows up to two stops.
STOPS_UP_TO_TWO = "3"

## @brief Name of the SerpApi flight provider.
PROVIDER_SERPAPI = "serpapi"

## @brief Name of the mock flight provider.
PROVIDER_MOCK = "mock"

## @brief Environment variable: Sheety endpoint of the "prices" sheet.
ENV_SHEETY_PRICES_ENDPOINT = "SHEETY_PRICES_ENDPOINT"

## @brief Environment variable: Sheety endpoint of the "users" sheet (the club's customers).
ENV_SHEETY_USERS_ENDPOINT = "SHEETY_USERS_ENDPOINT"

## @brief Environment variable: the Day 39 name of the prices endpoint, still accepted.
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

## @brief Environment variable: address of the SMTP server that sends the emails.
ENV_SMTP_ADDRESS = "SMTP_ADDRESS"

## @brief Environment variable: the sender's email address, also the SMTP login name.
ENV_EMAIL_ADDRESS = "EMAIL_ADDRESS"

## @brief Environment variable: the app password of the sender's email account.
ENV_EMAIL_PASSWORD = "EMAIL_PASSWORD"

## @brief Port of the SMTP server; the connection is upgraded with STARTTLS.
SMTP_PORT = 587

## @brief Subject line of the deal emails.
EMAIL_SUBJECT = "New Low Price Flight!"

## @brief Seconds pywhatkit waits for WhatsApp Web to load before it sends the message.
WHATSAPP_WAIT_SECONDS = 15

## @brief Seconds pywhatkit waits after sending before it closes the browser tab.
WHATSAPP_CLOSE_SECONDS = 3

## @brief Key that holds the rows in the Sheety response for the "prices" sheet.
PRICES_KEY = "prices"

## @brief Key that holds the rows in the Sheety response for the "users" sheet.
USERS_KEY = "users"

## @brief Field of a "users" row that holds the customer's email address.
EMAIL_FIELD = "email"

## @brief Pattern of an accepted email address: text, an at sign and a dotted domain.
EMAIL_PATTERN = r"[^@\s]+@[^@\s]+\.[^@\s]+"

## @brief Seconds to wait for an HTTP response before giving up.
REQUEST_TIMEOUT_SECONDS = 30

## @brief The longest piece of the flight service's error text that is printed.
ERROR_TEXT_MAX_LENGTH = 200
