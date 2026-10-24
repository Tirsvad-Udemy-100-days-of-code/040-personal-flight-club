# MIL-002 Flight data and indirect search

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Purpose

Decide whether the flight search handles destinations without direct flights (assignment Step 3).

## Deliverable

`FlightData` with a `stops` attribute; `FlightSearch.check_flights(origin_city_code, destination_city_code, from_time, to_time, is_direct=True)` using the SerpAPI `stops` parameter (and the mock provider's equivalent); `main.py` falling back to an indirect search with the assignment's console messages.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `FlightData.__init__()` takes `stops` and stores it; stops are computed as `len(flight["flights"]) - 1` | Unit tests pass | Missing or wrong |
| 2 | `check_flights(..., is_direct=True)` sends the nonstop filter, and `is_direct=False` sends the filter that allows 1 or 2 stops | Unit test on the request parameters | Wrong parameters |
| 3 | `main` prints "Getting direct flights for [city]..." and, when the price is "N/A", "No direct flight to [city]. Looking for indirect flights..." and searches with `is_direct=False` | Unit test with fakes | No fallback |
| 4 | No test uses the network or the real `.env` | Verified | Violated |

## Dependencies

| Depends on | Reason |
| --- | --- |
| MIL-001 | Builds on the previous phase |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| Objective 1 | [BC-001] Objectives |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-10-29 — within the two-week plan window of the Project Plan.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | FlightData stops | Add `stops` to `FlightData.__init__()` and to the "N/A" result. Compute `nr_stops = len(flight["flights"]) - 1` when parsing a response. | No | |
| 2 | check_flights with is_direct | Add the `is_direct=True` parameter. Direct: SerpAPI `stops=1` (nonstop only). Indirect: the SerpAPI value for up to 1 or 2 stops; the mock provider filters by number of stops. Pass the stops to `FlightData`. Keep the response cache. | No | |
| 3 | Indirect fallback in main | For each destination, search direct first; if `cheapest_flight.price == "N/A"`, print the fallback message and search again with `is_direct=False`. Keep the Day 39 price comparison, sheet update and WhatsApp message. | No | |
| 4 | Tests for stops and fallback | Unit tests for parsing the stops, the request parameters of both searches and the fallback logic, using fakes only. | No | |

---

[BC-001]: ../business-case.md
