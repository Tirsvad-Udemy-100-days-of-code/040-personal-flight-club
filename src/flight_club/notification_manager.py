"""
@file
@brief Builds low price alerts and sends them through email and WhatsApp.
"""

import os
import smtplib
from collections.abc import Callable
from email.message import EmailMessage

from flight_club.constants import (
    CURRENCY,
    EMAIL_SUBJECT,
    ENV_EMAIL_ADDRESS,
    ENV_EMAIL_PASSWORD,
    ENV_SMTP_ADDRESS,
    ENV_WHATSAPP_NUMBER,
    SMTP_PORT,
    WHATSAPP_CLOSE_SECONDS,
    WHATSAPP_WAIT_SECONDS,
)
from flight_club.flight_data import FlightData

_INSTALL_HINT = 'Install the optional extra with: pip install -e ".[whatsapp]"'
_NUMBER_HINT = f"Set {ENV_WHATSAPP_NUMBER} (with country code) to receive WhatsApp messages."
_EMAIL_HINT = (
    f"Set {ENV_SMTP_ADDRESS}, {ENV_EMAIL_ADDRESS} and {ENV_EMAIL_PASSWORD} to send emails."
)


## @brief Formats flight alerts and delivers them by email to the customers and to the owner's WhatsApp.
class NotificationManager:
    ## @brief Reads every setting from the environment, in this one place.
    #  @param sender Callable taking (number, message); used instead of pywhatkit when given.
    def __init__(self, sender: Callable[[str, str], None] | None = None) -> None:
        self._sender = sender
        self._smtp_address = os.environ.get(ENV_SMTP_ADDRESS)
        self._email_address = os.environ.get(ENV_EMAIL_ADDRESS)
        self._email_password = os.environ.get(ENV_EMAIL_PASSWORD)
        self._whatsapp_number = os.environ.get(ENV_WHATSAPP_NUMBER)

    ## @brief Builds the alert text for one cheap flight.
    #
    #  A direct flight gets the short text; a flight with stopovers says how many.
    #  The price uses the currency code (GBP), never a currency symbol.
    #  @param flight The cheapest flight found for a destination.
    #  @return A one line message with price, airports and both dates.
    def build_message(self, flight: FlightData) -> str:
        message = (
            f"Low price alert! Only {CURRENCY} {flight.price} to fly "
            f"from {flight.origin_airport} to {flight.destination_airport}, "
            f"from {flight.out_date} to {flight.return_date}."
        )
        if flight.stops == 0:
            return message
        noun = "stopover" if flight.stops == 1 else "stopovers"
        return f"{message} Flight has {flight.stops} {noun}."

    ## @brief Sends the message to every address; never raises.
    #
    #  The mail is encoded as UTF-8, so non-ASCII characters do not fail.
    #  @param email_list Recipient addresses.
    #  @param email_body The text of the mail.
    #  @return The number of mails that were sent; 0 when the SMTP settings are missing.
    def send_emails(self, email_list: list[str], email_body: str) -> int:
        if not email_list:
            return 0
        if not (self._smtp_address and self._email_address and self._email_password):
            print(_EMAIL_HINT)
            print(email_body)
            return 0
        sent = 0
        try:
            with smtplib.SMTP(self._smtp_address, SMTP_PORT) as connection:
                connection.starttls()
                connection.login(self._email_address, self._email_password)
                for address in email_list:
                    connection.send_message(self._build_email(address, email_body))
                    sent += 1
        except (smtplib.SMTPException, OSError) as error:
            # Only the type is printed: the text of the error might echo the login.
            print(f"Sending email failed: {type(error).__name__}.")
        return sent

    def _build_email(self, address: str, email_body: str) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = EMAIL_SUBJECT
        message["From"] = self._email_address
        message["To"] = address
        message.set_content(email_body, charset="utf-8")
        return message

    ## @brief Sends a message to the number in the environment; never raises.
    #  @param message The text to send.
    #  @return True when sent, False when it was only printed.
    def send_whatsapp(self, message: str) -> bool:
        number = self._whatsapp_number
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
