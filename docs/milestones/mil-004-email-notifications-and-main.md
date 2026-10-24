# MIL-004 Email notifications and main program

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c5a6ed5] |

---

## Purpose

Decide whether customers receive the flight deal by email (assignment Step 5).

## Deliverable

`NotificationManager` that reads all its environment variables (SMTP address, email, app password, WhatsApp number) in `__init__()` and has `send_emails()`; `main.py` crafts a direct-flight or a stopover message and sends it to all customers.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `NotificationManager.__init__()` reads every environment variable in one place | Verified in code and test | Variables read elsewhere |
| 2 | `send_emails(email_list, message)` logs in through `smtplib` with the app password and sends to every address, UTF-8 encoded | Unit test with a fake `smtplib.SMTP` | Fails |
| 3 | `main` writes a different message for a direct flight and for a flight with a stopover; the text uses "GBP" and holds price, origin, destination, dates and, for a stopover, the number of stops | Unit test on the text | Same text or "£" used |
| 4 | No test sends mail or reads the real `.env` | Verified | Violated |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-003 | Builds on the previous phase |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 2 and 3 | [BC-001] Objectives |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-04 — within the two-week plan window of the Project Plan.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | SMTP settings in NotificationManager | Read `SMTP_ADDRESS`, `EMAIL_ADDRESS`, `EMAIL_PASSWORD` and the WhatsApp number in `__init__()`; add them to `.env.example`. The SMTP port is a constant. | No | |
| 2 | send_emails | Implement `send_emails(email_list, email_body)` with `smtplib` and STARTTLS; build the message as UTF-8 so non-ASCII characters do not fail; one message per customer, with a subject line. | No | |
| 3 | Message text in main | Craft the direct and stopover messages (stops in the stopover text) using "GBP"; send the WhatsApp message and the emails when a cheaper flight is found. | No | |
| 4 | Tests for email and messages | Unit tests with a fake SMTP class and tests of both message texts. | No | |

---

[BC-001]: ../business-case.md
[c5a6ed5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/c5a6ed5985f76d8836f763acc5638053a39157f2
