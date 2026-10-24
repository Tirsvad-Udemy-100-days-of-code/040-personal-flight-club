# MIL-003 Customer emails

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c5a6ed5] |

---

## Purpose

Decide whether the customer list can be read from the second sheet (assignment Step 4).

## Deliverable

`DataManager` that reads all environment variables (token, prices endpoint, users endpoint) in `__init__()` and has `get_customer_emails()` returning the data of the "users" sheet; `.env.example` lists the new endpoint.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `DataManager.__init__()` reads every environment variable in one place | Verified in code and test | Variables read elsewhere |
| 2 | `get_customer_emails()` returns the users' data and the list of email addresses | Unit test with a fake response | Fails |
| 3 | `.env.example` lists the prices and users endpoints without values | Present | Missing |
| 4 | No test uses the network or the real `.env` | Verified | Violated |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-002 | Builds on the previous phase |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 2 | [BC-001] Objectives |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-31 — within the two-week plan window of the Project Plan.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Settings in DataManager.__init__ | Read `SHEETY_PRICES_ENDPOINT`, `SHEETY_USERS_ENDPOINT` and the authentication variables in `__init__()`. Keep `SHEETY_ENDPOINT` working as a fallback for the prices endpoint so Day 39 `.env` files keep running. | No | |
| 2 | get_customer_emails | Add `get_customer_emails()` that returns the rows of the "users" sheet and a helper that extracts the email addresses (column name from a constant, `email`), skipping rows without a valid-looking address. | No | |
| 3 | Tests for DataManager | Unit tests with a fake `requests` session for both sheets. | No | |
| 4 | Env template | Add the users endpoint to `.env.example`. | No | |

---

[BC-001]: ../business-case.md
[c5a6ed5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/c5a6ed5985f76d8836f763acc5638053a39157f2
