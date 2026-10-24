# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-010 |
| CrossReference | [MIL-003], [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Artifact Under Review

- Instance reviewed: [MIL-003] (the Python code and tests of its tasks 1 to 4: `src/flight_club/`, `tests/`)
- Checklist used: [QC-PY-001]
- Scope: full review of the code changed by this milestone
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Names use snake_case, PascalCase and UPPER_SNAKE (`ENV_SHEETY_USERS_ENDPOINT`, `extract_emails`). |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`get_customer_emails`, `extract_emails`, `EMAIL_PATTERN`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check` and `ruff format --check` pass; no new suppressions. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every new function and test has annotations including `-> None`. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare except; HTTP and shape problems raise `DataManagerError` with specific messages. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults and no shadowed builtins; `_read_rows` is shared by both sheets. |
| 7 | Files, locks and connections are managed with context managers | Pass | No files or connections opened by the new code; the HTTP session is unchanged. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public classes and functions carry Doxygen comments (what, not how). |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | Console output uses `print` as the assignment requires; recorded in [ADR-0001]. No secrets are printed. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No DCD exists; the assignment's classes are the design; deviation recorded in [ADR-0001]. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | New behaviour is tested: users read, errors, missing users endpoint, email extraction, legacy endpoint name. Fakes only; no network or `.env`. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes on `src` and `tests`; the only `Any` is the JSON response shape. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | No new dependencies. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | One private `_read_rows` serves both sheets; endpoint names, keys and the email pattern are constants. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `flight_data` imports only `constants`; `main` wires the others; no import cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `get_destination_data` and `update_lowest_price` keep their contracts; the users endpoint is checked only when used, so Day 39 `.env` files still run. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Flat layout accepted by [ADR-0001] (merged layers). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File names are lower-case snake_case English with no spaces. |

## Overall Verdict

Go — all mandatory criteria pass; deviations are recorded in ADR-0001.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | - | - |

---

[MIL-003]: ../../milestones/mil-003-customer-emails.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-flat-module-layout-and-console-output.md
