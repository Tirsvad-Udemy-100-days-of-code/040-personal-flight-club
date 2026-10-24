import builtins
import sys
import types
from typing import Any

import pytest

from flight_club.constants import ENV_WHATSAPP_NUMBER
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
