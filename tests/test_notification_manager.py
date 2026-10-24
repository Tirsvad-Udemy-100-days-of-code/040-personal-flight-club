import builtins
import smtplib
import sys
import types
from typing import Any, ClassVar, Self

import pytest

from flight_club.constants import (
    ENV_EMAIL_ADDRESS,
    ENV_EMAIL_PASSWORD,
    ENV_SMTP_ADDRESS,
    ENV_WHATSAPP_NUMBER,
    SMTP_PORT,
)
from flight_club.flight_data import FlightData
from flight_club.notification_manager import NotificationManager

NUMBER = "+441234567890"


def _flight() -> FlightData:
    return FlightData(54, "LHR", "CDG", "2026-10-25", "2027-04-20")


def test_build_message_contains_price_airports_and_dates() -> None:
    message = NotificationManager().build_message(_flight())
    assert message == (
        "Low price alert! Only GBP 54 to fly from LHR to CDG, from 2026-10-25 to 2027-04-20."
    )


def test_send_whatsapp_returns_false_when_number_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv(ENV_WHATSAPP_NUMBER, raising=False)
    assert NotificationManager().send_whatsapp("hello") is False
    output = capsys.readouterr().out
    assert "hello" in output
    assert ENV_WHATSAPP_NUMBER in output


def test_send_whatsapp_uses_injected_sender(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_WHATSAPP_NUMBER, NUMBER)
    calls: list[tuple[str, str]] = []
    manager = NotificationManager(sender=lambda number, message: calls.append((number, message)))
    assert manager.send_whatsapp("hello") is True
    assert calls == [(NUMBER, "hello")]


def test_send_whatsapp_returns_false_when_pywhatkit_missing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv(ENV_WHATSAPP_NUMBER, NUMBER)
    monkeypatch.delitem(sys.modules, "pywhatkit", raising=False)
    real_import = builtins.__import__

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "pywhatkit":
            raise ImportError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert NotificationManager().send_whatsapp("hello") is False
    output = capsys.readouterr().out
    assert "whatsapp" in output
    assert "hello" in output
    assert NUMBER not in output


def test_send_whatsapp_never_prints_number_when_pywhatkit_fails(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv(ENV_WHATSAPP_NUMBER, NUMBER)
    fake = types.ModuleType("pywhatkit")

    def fail(*args: Any) -> None:
        raise RuntimeError(f"cannot reach {args[0]}")

    fake.sendwhatmsg_instantly = fail  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pywhatkit", fake)
    assert NotificationManager().send_whatsapp("hello") is False
    output = capsys.readouterr().out
    assert "RuntimeError" in output
    assert "hello" in output
    assert NUMBER not in output


def test_send_whatsapp_calls_pywhatkit_with_documented_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENV_WHATSAPP_NUMBER, NUMBER)
    received: list[tuple[Any, ...]] = []
    fake = types.ModuleType("pywhatkit")
    fake.sendwhatmsg_instantly = lambda *args: received.append(args)  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "pywhatkit", fake)
    assert NotificationManager().send_whatsapp("hello") is True
    assert received == [(NUMBER, "hello", 15, True, 3)]


SMTP_HOST = "smtp.example.test"
SENDER = "club@example.test"
APP_PASSWORD = "app-password-secret"


class FakeSMTP:
    """Stands in for smtplib.SMTP; records what the manager does and sends nothing."""

    instances: ClassVar[list["FakeSMTP"]] = []
    fail_with: ClassVar[Exception | None] = None

    def __init__(self, host: str, port: int) -> None:
        if FakeSMTP.fail_with is not None:
            raise FakeSMTP.fail_with
        self.host = host
        self.port = port
        self.started_tls = False
        self.login_args: tuple[str, str] | None = None
        self.messages: list[Any] = []
        FakeSMTP.instances.append(self)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def starttls(self) -> None:
        self.started_tls = True

    def login(self, user: str, password: str) -> None:
        self.login_args = (user, password)

    def send_message(self, message: Any) -> None:
        self.messages.append(message)


@pytest.fixture
def smtp(monkeypatch: pytest.MonkeyPatch) -> type[FakeSMTP]:
    FakeSMTP.instances = []
    FakeSMTP.fail_with = None
    monkeypatch.setenv(ENV_SMTP_ADDRESS, SMTP_HOST)
    monkeypatch.setenv(ENV_EMAIL_ADDRESS, SENDER)
    monkeypatch.setenv(ENV_EMAIL_PASSWORD, APP_PASSWORD)
    monkeypatch.setattr(smtplib, "SMTP", FakeSMTP)
    return FakeSMTP


def test_send_emails_logs_in_and_sends_one_mail_per_address(smtp: type[FakeSMTP]) -> None:
    sent = NotificationManager().send_emails(["a@example.test", "b@example.test"], "deal")
    connection = smtp.instances[0]
    assert sent == 2
    assert (connection.host, connection.port) == (SMTP_HOST, SMTP_PORT)
    assert connection.started_tls
    assert connection.login_args == (SENDER, APP_PASSWORD)
    assert [m["To"] for m in connection.messages] == ["a@example.test", "b@example.test"]
    assert all(m["From"] == SENDER for m in connection.messages)
    assert connection.messages[0].get_content().strip() == "deal"


def test_send_emails_encodes_non_ascii_text_as_utf8(smtp: type[FakeSMTP]) -> None:
    NotificationManager().send_emails(["a@example.test"], "Only £54 to Zürich")
    message = smtp.instances[0].messages[0]
    assert "£54 to Zürich" in message.get_content()
    assert message.get_content_charset() == "utf-8"
    assert "£54".encode() in message.as_bytes()


def test_send_emails_without_recipients_does_not_connect(smtp: type[FakeSMTP]) -> None:
    assert NotificationManager().send_emails([], "deal") == 0
    assert smtp.instances == []


@pytest.mark.parametrize("name", [ENV_SMTP_ADDRESS, ENV_EMAIL_ADDRESS, ENV_EMAIL_PASSWORD])
def test_send_emails_prints_instead_when_a_setting_is_missing(
    smtp: type[FakeSMTP],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    name: str,
) -> None:
    monkeypatch.delenv(name)
    assert NotificationManager().send_emails(["a@example.test"], "deal") == 0
    output = capsys.readouterr().out
    assert "deal" in output
    assert name in output
    assert smtp.instances == []


def test_send_emails_never_raises_or_prints_the_login_when_smtp_fails(
    smtp: type[FakeSMTP], capsys: pytest.CaptureFixture[str]
) -> None:
    smtp.fail_with = smtplib.SMTPAuthenticationError(535, f"bad login {APP_PASSWORD}".encode())
    assert NotificationManager().send_emails(["a@example.test"], "deal") == 0
    output = capsys.readouterr().out
    assert "SMTPAuthenticationError" in output
    assert APP_PASSWORD not in output


def test_build_message_for_a_direct_flight_has_no_stopover_text() -> None:
    assert "stopover" not in NotificationManager().build_message(_flight())


@pytest.mark.parametrize(("stops", "text"), [(1, "1 stopover."), (2, "2 stopovers.")])
def test_build_message_for_a_stopover_flight_says_how_many(stops: int, text: str) -> None:
    flight = FlightData(540, "LHR", "DPS", "2026-10-25", "2027-04-20", stops)
    message = NotificationManager().build_message(flight)
    assert message.endswith(f"Flight has {text}")
    assert message != NotificationManager().build_message(_flight())


def test_messages_use_gbp_and_not_the_pound_sign() -> None:
    flight = FlightData(540, "LHR", "DPS", "2026-10-25", "2027-04-20", 1)
    for message in (
        NotificationManager().build_message(flight),
        NotificationManager().build_message(_flight()),
    ):
        assert "GBP" in message
        assert "£" not in message
