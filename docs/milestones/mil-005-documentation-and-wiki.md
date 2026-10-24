# MIL-005 Documentation and wiki

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c5a6ed5] |

---

## Purpose

Decide whether the repository is ready for participants and visitors.

## Deliverable

README from the framework template with run and test instructions and screenshots; wiki pages in English, Danish and Bahasa Malaysia with screenshots; Doxygen check; `.venv` and `python -m pip install --upgrade pip` instructions.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | README follows the framework template and `check-readme.sh` passes | Passes | Fails |
| 2 | README documents creating and using `.venv` and `python -m pip install --upgrade pip`, running the program and running the tests | Present | Missing |
| 3 | Wiki pages exist in en, da and ms, each with a screenshot | All present | Any missing |
| 4 | `doxygen` runs with the Doxyfile without errors | No errors | Errors |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-004 | Builds on the previous phase |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 5 | [BC-001] Objectives |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-07 — within the two-week plan window of the Project Plan.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Screenshots | Capture a sample run (mock data, no real addresses) and a test run, as images in `docs/images/`. Never show tokens or real email addresses. | No | |
| 2 | README | Fill the framework README template: description, features, installation with `.venv` and `python -m pip install --upgrade pip`, `.env` setup, usage, tests, screenshots, licence. | No | |
| 3 | Wiki in three languages | Write Home and Getting-Started pages in English, Danish and Bahasa Malaysia under `docs/wiki/`, with a sidebar, for the publish workflow. | No | |
| 4 | Doxygen check | Run Doxygen on the Doxyfile and fix warnings in the source comments. | No | |

---

[BC-001]: ../business-case.md
[c5a6ed5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/c5a6ed5985f76d8836f763acc5638053a39157f2
