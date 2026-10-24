# MIL-001 Baseline and project setup

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | [c5a6ed5] |

---

## Purpose

Decide whether the repository skeleton is ready for the Day 40 changes: Day 39 code carried over, tooling, configuration, secrets handling, CI and repository metadata.

## Deliverable

A Python 3.13+ project: pyproject.toml, src/ and tests/ layout with the Day 39 code and tests, constants.py, .gitignore, .env.example, Doxyfile, venv instructions, framework hooks, CI workflows from TirSystem/github-action, and the repository description and topics.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `pytest` runs in a fresh `.venv` and passes the carried-over Day 39 tests | Passes | Fails |
| 2 | `.env` and cache files are ignored; only `.env.example` is tracked | Verified with `git check-ignore` | Secret tracked |
| 3 | Installed CI workflows are present and pass on the pull request | Green | Red after 3 fixes |
| 4 | Repository description and at least 5 topics are set | Set | Missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| None | First phase; the baseline documents (BC, SA, PP) are accepted before it |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objectives 4 and 5 | [BC-001] Objectives |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-26 — within the two-week plan window of the Project Plan.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Carry over the Day 39 code | Copy `src/flight_club/` and `tests/` from the `039-personal-flight-club` repository (same package and names) into this project and set the project name and description for Day 40 in `pyproject.toml` (Python >=3.13; runtime dependencies requests, requests-cache, python-dotenv; extras `whatsapp` and `dev`). Use `constants.py` for constants. Do not copy `.env`, caches or `.venv`. | No | |
| 2 | Ignore file and env template | Add a Python `.gitignore` (also `.env`, `flight_cache.sqlite`, `.venv`, Doxygen output) and `.env.example` listing variable names without values. The real `.env` holds the participant's tokens and is never committed, tested or read by tests. | No | |
| 3 | Doxygen configuration | Add a `Doxyfile` that scans `src/` and writes to a git-ignored folder; source files use Doxygen comments. | No | |
| 4 | Install CI workflows | Install the workflows that fit from https://git.tirsystem.com/TirSystem/github-action (tests, quality, English-comments check, wiki publish, milestone sync) into `.gitea/workflows/`. Stop and report if they cannot fit. | No | |
| 5 | Framework git hooks | Run `install-git-hooks.sh` with the plan gate enabled so commits to src/ and tests/ need a Task trailer. | No | |
| 6 | Repository description and topics | Set the description and topics on the `040-personal-flight-club` repository through the host API with the local `GITEA_TOKEN`, read from `.env` by a script and never printed or put on a command line. | No | |

---

[BC-001]: ../business-case.md
[c5a6ed5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/040-personal-flight-club/commit/c5a6ed5985f76d8836f763acc5638053a39157f2
