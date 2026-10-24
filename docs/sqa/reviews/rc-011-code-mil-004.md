# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-011 |
| CrossReference | [MIL-004], [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [d94a68a] |

---

## Artifact Under Review

- Instance reviewed: [MIL-004] (the Python code and tests of its tasks 1 to 4: `src/flight_club/`, `tests/`)
- Checklist used: [QC-PY-001]
- Scope: full review of the code changed by this milestone
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Names use snake_case, PascalCase and UPPER_SNAKE (`send_emails`, `ENV_SMTP_ADDRESS`, `SMTP_PORT`). |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`send_emails`, `_build_email`, `EMAIL_SUBJECT`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass; no new suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every new function and test has annotations including `-> None`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Only `smtplib.SMTPException` and `OSError` are caught, in one place; the error type is reported and the loop result is returned, nothing is swallowed silently. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults (`is_direct: bool = True`, `stops: int = 0`); no shadowed builtins. |
| 7 | Files, locks and connections are managed with context managers | Pass | The SMTP connection is opened with a `with` block, so it is always closed. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public classes and functions carry Doxygen comments (what, not how). |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | Output uses `print` as the program's console output, recorded in [ADR-0001]. The SMTP error text and the app password are never printed (test `never_raises_or_prints_the_login`). |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No DCD exists; the assignment's classes are the design; deviation recorded in [ADR-0001]. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | New behaviour is tested with a fake `smtplib.SMTP`: login and STARTTLS, one mail per address, UTF-8 body, missing settings, SMTP failure, both message texts, GBP and no pound sign, customers read once, WhatsApp still sent when customers cannot be read. No mail is sent; no `.env`. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes on `src` and `tests`; the only `Any` is the JSON response shape. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | No new dependencies. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The message text is built in one place (`build_message`) and reused for WhatsApp and email; env names, port and subject are constants. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `flight_data` imports only `constants`; `main` wires the others; no import cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `send_emails` is added next to `send_whatsapp` without changing it; the SMTP class is the standard one and is replaced in tests by monkeypatching. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Flat layout accepted by [ADR-0001] (merged layers). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File names are lower-case snake_case English with no spaces. |

## Overall Verdict

Go — all mandatory criteria pass; deviations are recorded in ADR-0001.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | - | - |

---

[MIL-004]: ../../milestones/mil-004-email-notifications-and-main.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-flat-module-layout-and-console-output.md
[d94a68a]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/d94a68ac10edbcbd44b59f8f1f30c5aa14a9edb8
