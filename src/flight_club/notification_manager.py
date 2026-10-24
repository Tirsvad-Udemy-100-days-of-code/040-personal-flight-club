"""
@file
@brief Builds low price alerts and sends them through WhatsApp.
"""

import os
from collections.abc import Callable

from flight_club.constants import (
    CURRENCY,
    ENV_WHATSAPP_NUMBER,
    WHATSAPP_CLOSE_SECONDS,
    WHATSAPP_WAIT_SECONDS,
)
from flight_club.flight_data import FlightData

_INSTALL_HINT = 'Install the optional extra with: pip install -e ".[whatsapp]"'
_NUMBER_HINT = f"Set {ENV_WHATSAPP_NUMBER} (with country code) to receive WhatsApp messages."


## @brief Formats flight alerts and delivers them to the owner's WhatsApp.
class NotificationManager:
    ## @brief Creates the manager with an optional replacement for pywhatkit.
    #  @param sender Callable taking (number, message); used instead of pywhatkit when given.
    def __init__(self, sender: Callable[[str, str], None] | None = None) -> None:
        self._sender = sender

    ## @brief Builds the alert text for one cheap flight.
    #  @param flight The cheapest flight found for a destination.
    #  @return A one line message with price, airports and both dates.
    def build_message(self, flight: FlightData) -> str:
        return (
            f"Low price alert! Only {CURRENCY} {flight.price} to fly "
            f"from {flight.origin_airport} to {flight.destination_airport}, "
            f"from {flight.out_date} to {flight.return_date}."
        )

    ## @brief Sends a message to the number in the environment; never raises.
    #  @param message The text to send.
    #  @return True when sent, False when it was only printed.
    def send_whatsapp(self, message: str) -> bool:
        number = os.environ.get(ENV_WHATSAPP_NUMBER)
        if not number:
            return self._print_instead(_NUMBER_HINT, message)
        if self._sender is not None:
            return self._send_with(self._sender, number, message)
        try:
            import pywhatkit  # type: ignore[import-not-found,unused-ignore]
        except ImportError:
            return self._print_instead(_INSTALL_HINT, message)
        return self._send_with(self._pywhatkit_sender(pywhatkit), number, message)

    @staticmethod
    def _pywhatkit_sender(module: object) -> Callable[[str, str], None]:
        def send(number: str, message: str) -> None:
            module.sendwhatmsg_instantly(  # type: ignore[attr-defined]
                number, message, WHATSAPP_WAIT_SECONDS, True, WHATSAPP_CLOSE_SECONDS
            )

        return send

    @staticmethod
    def _send_with(sender: Callable[[str, str], None], number: str, message: str) -> bool:
        try:
            sender(number, message)
        except Exception as error:  # noqa: BLE001
            # Only the type is printed: the text of the error might echo the phone number.
            print(f"WhatsApp message failed: {type(error).__name__}.")
            print(message)
            return False
        return True

    @staticmethod
    def _print_instead(hint: str, message: str) -> bool:
        print(hint)
        print(message)
        return False
