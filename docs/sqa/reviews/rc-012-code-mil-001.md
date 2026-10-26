# SQA Review Record

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-012 |
| CrossReference | [MIL-001], [QC-PY-001], [ADR-0001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [3eb3531] |

---

## Artifact Under Review

- Instance reviewed: [MIL-001] (the Python code and tests of its task 1: `src/flight_club/`, `tests/`)
- Checklist used: [QC-PY-001]
- Scope: full review of the code changed by this milestone
- Mode: autonomous, not independent (the reviewer is `AI as stand-in for S01`)

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | The Day 39 code uses snake_case, PascalCase and UPPER_SNAKE throughout. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`DataManager`, `find_cheapest_flight`, `REQUEST_TIMEOUT_SECONDS`). |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check`, `ruff format --check` pass on the carried-over code. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function carries annotations; `mypy --strict` passes. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | Failures raise `DataManagerError` or `FlightSearchError`, or print the error type; nothing is silently swallowed. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable defaults; no shadowed builtins. |
| 7 | Files, locks and connections are managed with context managers | Pass | No files are opened by the code; HTTP sessions are injected or created per call. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Public classes and functions carry Doxygen comments (what, not how). |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | Console output uses `print` as the assignment requires; recorded in [ADR-0001]. No secrets are printed. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No DCD exists; the assignment's classes are the design; deviation recorded in [ADR-0001]. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | The 68 carried-over tests cover every module, use fakes, and need no network or `.env`. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; `Any` is used only for decoded JSON. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | No new dependencies. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Constants live in `constants.py`; one place per rule. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `flight_data` imports only `constants`; `main` wires the others; no import cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Collaborators are injected into `main.run`, so each class has one reason to change. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | Flat layout accepted by [ADR-0001] (merged layers). |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | File names are lower-case snake_case English with no spaces. |

## Overall Verdict

Go — all mandatory criteria pass; deviations are recorded in ADR-0001.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | - | - |

---

[MIL-001]: ../../milestones/mil-001-baseline-and-setup.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[ADR-0001]: ../../adr/adr-0001-flat-module-layout-and-console-output.md
[3eb3531]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/3eb353140bdce71580a9d8a60acb42fdc8ca9d54
