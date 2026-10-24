# Stakeholder Analysis

## Metadata
| Key | Value |
| --- | --- |
| ID | SA-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

This analysis names the people the flight club serves, so owners, reviewers and the documentation can cite stable IDs. It uses the Power/Interest grid.

## Stakeholder Summary Table

| ID | Name | Role/Title | Organization | Power Level | Interest Level | Quadrant | Primary Concern (Business Language) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | Jens Tirsvad Nielsen | Course participant; Product Owner, developer and reviewer | Private | HIGH | HIGH | Manage Closely | A working, well-documented lesson solution that is cheap to run |
| S02 | Udemy coursists | Fellow course participants | Udemy course community | LOW | MEDIUM | Keep Informed | Readable, runnable code with the assignment's function names, and README run instructions |
| S03 | GitHub viewers | Repository visitors | Public | LOW | LOW | Monitor | A clear description, topics and README, and no extra runtime dependencies |

## Power/Interest Classification Rationale

- **Manage Closely (S01):** decides scope, writes and reviews everything.
- **Keep Informed (S02):** cannot change the project, but copies and compares the code, so readability and instructions matter.
- **Monitor (S03):** casual visitors; the repository front page is enough.

## Primary Concerns and FURPS+ Mapping

| ID | Concern | FURPS+ attribute |
| --- | --- | --- |
| S01 | Emails and messages carry correct deal data, with stops | Functionality |
| S01 | Free-tier quotas are not wasted | Performance |
| S01 | Secrets stay out of the repository; no mail to real people from tests | Functionality (security) |
| S02 | Assignment names kept; code readable | Supportability |
| S02 | Run steps work on a fresh clone | Usability |
| S03 | Description, topics, README, wiki in three languages | Usability |
| S03 | No runtime dependencies beyond the assignment | Supportability |

## Communication Requirements

| ID | Channel | Frequency | Deliverable | Phase / Milestone |
| --- | --- | --- | --- | --- |
| S01 | Chat and run summary | Per milestone | Run summary with RC records and stand-in decisions | All |
| S02 | README and wiki | On release | Run instructions, wiki pages | MIL-005 |
| S03 | Repository page | On release | Description, topics, README, screenshots | MIL-001, MIL-005 |

## Conflicting Interests and Mitigations

| Conflict | Stakeholders | Mitigation |
| --- | --- | --- |
| S02 wants the assignment's structure; clean architecture would reshape it | S01, S02 | Keep the assignment's class and function names; put them in thin modules over a small `src/` package |
| S03 wants no dependencies; WhatsApp and caching need packages | S01, S03 | Runtime: `requests`, `requests_cache`, `python-dotenv`; WhatsApp module optional and lazy; SMTP uses the standard library; dev tools only in the dev extra |

## Traceability Analysis

### Business Goal Alignment

| Stakeholder | Concern | Business Case objective |
| --- | --- | --- |
| S01 | Correct deals, quota, secrets | [BC-001] objectives 1 to 4 |
| S02 | Readable, runnable code | [BC-001] objectives 2, 3 and 5 |
| S03 | Findable repository | [BC-001] objective 5 |

## Sign-Off

Reviewer: S01 (the AI acts as stand-in in autonomous mode, recorded in the RC record).

---

[BC-001]: ./business-case.md
