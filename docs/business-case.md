# Business Case

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Executive Summary

Day 40 of Udemy's "100 Days of Code: The Complete Python Pro Bootcamp" turns the Day 39 flight-deal finder into a small flight club. The program now searches direct flights first and falls back to flights with stopovers, reads a customer list from a second Google Sheet ("users"), and sends every customer an email with the deal through SMTP. This project delivers that program as a tested, documented Python 3.13+ repository, built on the code of the `039-personal-flight-club` repository, for the course participant and for other participants who compare solutions.

## Methodological and Standards Foundation

The work follows the SQA and QC framework mounted at `framework/`: artifacts are reviewed against QC checklists tagged with ISO/IEC 25010:2023 characteristics, and code follows the `coding-conventions` and `clean-architecture` skills. Source code carries Doxygen comments and is tested with pytest.

## Problem Statement

The Day 39 program reports only the cheapest flight found, and says nothing about stopovers. Many popular destinations have no direct flight, so they are reported as "N/A". The deals reach only the participant, by WhatsApp; the club's customers, who sign up in a Google Form, get nothing. The starter files of the lesson use Twilio, which this participant replaced in Day 39 and does not want to bring back.

## Business Opportunity

A club that mails every member the best deal, direct or with stops, is a complete small product and a portfolio piece. Other participants (S02) and GitHub visitors (S03) get readable code with the assignment's function names and clear run instructions.

## Objectives

1. Search direct flights first (`check_flights(..., is_direct=True)`); when none is found, search again with stopovers, and record the number of stops in `FlightData.stops`.
2. Read the customer emails from the "users" sheet with `DataManager.get_customer_emails()`; all environment variables, including both sheet endpoints, are read in `DataManager.__init__()`.
3. Send every customer an email through SMTP with `NotificationManager.send_emails()`, with a different message for a direct flight and for a flight with a stopover; the text uses "GBP" and is encoded as UTF-8.
4. Keep every secret in `.env` and never in the repository; keep the Day 39 response cache so free-tier quotas last.
5. Publish a documented repository: README with screenshots, wiki in English, Danish and Bahasa Malaysia with screenshots, Doxygen configuration, CI workflows, description and topics.

## Scope

### In Scope

- A Python 3.13+ project with `src/` and `tests/`, `pyproject.toml`, a local `.venv`, pytest, `constants.py`, a Doxyfile and a Python `.gitignore`, starting from the Day 39 code.
- The assignment's classes and names: `DataManager` with `get_customer_emails()`, `FlightSearch.check_flights()` with `is_direct`, `FlightData` with `stops`, `NotificationManager.send_emails()`, and `main.py`.
- The WhatsApp message of Day 39 stays; the email is added next to it.
- README from the framework template, a three-language wiki, screenshots, CI workflows from the TirSystem workflow repository, repository description and topics.

### Out of Scope

- Twilio SMS or WhatsApp, which the Day 39 project replaced.
- A sign-up form or website (the Google Form is outside the repository) and email address validation beyond a basic format check.
- Automated tests that call the real Sheety, SerpAPI, mock-flight, SMTP or WhatsApp services, or that read the real `.env`.
- A database, scheduling of the daily run, unsubscribe handling and booking of flights.

## Expected Benefits

### Tangible Benefits

- A working, runnable lesson solution with automated tests.
- A repository other participants can clone and run from the README alone.

### Intangible Benefits

- Practice with `smtplib`, environment secrets, API fallbacks and a second data source.
- A reusable template for later course days.

## Strategic Alignment

The project supports the participant's learning goal (completing the bootcamp) and the shared goal of publishing readable solutions that others can learn from.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| 1 | Unit tests pass | 100% of tests pass, no network or `.env` access | `pytest` exit code 0 |
| 2 | Indirect fallback | When the direct search finds nothing, a search with stops runs and `stops` is set | Unit test on `main` and `check_flights` |
| 3 | Customer emails | `get_customer_emails()` returns the list of addresses from the users sheet | Unit test with a fake HTTP response |
| 4 | Email content | Direct and stopover messages differ; text holds price, origin, destination, dates, stops and no "£" | Unit test on the message text |
| 5 | Run instructions work | A fresh clone runs by following the README steps only | Manual run of the README steps |
| 6 | Repository metadata and wiki | Description and at least 5 topics set; en, da and ms wiki pages with screenshots | Check on the git host and file review |
| 7 | Runtime dependencies | Only packages the assignment needs; none added over Day 39 | `pyproject.toml` review |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Free-tier quotas run out (SerpAPI 100/month, Sheety 200/month) | Development stops | Keep the response cache; use the mock flight service; keep 3 to 5 destinations; the extra indirect search runs only when no direct flight exists |
| Secrets committed by mistake | Credential leak | `.env` and cache files in `.gitignore`; only `.env.example` committed; secret scan before each PR |
| SMTP credentials are not yet in the local `.env` | Real mails cannot be sent | SMTP is isolated in `NotificationManager`; tests use a fake `smtplib`; the missing values are an open issue in the Project Plan |
| Mails sent to real customers by mistake during development | Spam to real people | Tests never send; README tells the participant to use a test sheet first |
| CI workflows from the TirSystem repository do not fit this project | Red pipeline | Install only the needed workflows; stop and report after three failed fixes |

## Assumptions

- The Day 39 code is the base. Its WhatsApp delivery (`pywhatkit`, optional and lazy) and the mock flight service remain; Twilio is not restored.
- The Sheety project exposes a `prices` sheet (`city`, `iataCode`, `lowestPrice`, `id`) and a `users` sheet filled by a Google Form (`firstName`, `lastName`, `email`); both use Bearer authentication.
- The participant (S01) is Product Owner, developer and reviewer; in autonomous mode the AI acts as stand-in reviewer and every such review says so.
- The origin airport is LHR and the currency is GBP, both constants, as in the assignment.
- Real tokens exist only in the participant's local `.env`, are used by the participant's own runs and by the repository setup on the git host, and never by tests. The AI uses only the git host token, to set the description and topics.

## Constraints

- Python 3.13 or newer; `venv`; pytest; a `constants.py` for constants; `pyproject.toml` for configuration.
- Doxygen comments in source and a Doxyfile.
- Hosted at `https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code` (this project is the `040-personal-flight-club` repository); one branch and pull request per step.
- No more runtime dependencies than needed; `smtplib` is part of the standard library.

## Cost–Benefit Assessment

| Costs | Benefits |
| --- | --- |
| The participant's spare time; free-tier API accounts; AI assistance | A finished lesson solution, a portfolio repository and a reusable template. Qualitative assessment: the project is small and the cost is time only. |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Finish the lesson, own the product and review it |
| S02 | Compare solutions; runnable code with the assignment's names |
| S03 | Browse for ideas; clear description, topics and README |

## Recommendation

Proceed — the scope is small, builds on working Day 39 code, the risks are mitigated, and the result serves all three stakeholders.

---

[SA-001]: ./stakeholder-analysis.md
