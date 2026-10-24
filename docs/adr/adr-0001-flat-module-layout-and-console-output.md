# Keep the assignment's flat module layout and console output

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-24 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The Day 40 program is an assignment solution. Stakeholder S02 wants the assignment's file and class names (`main.py`, `data_manager.py`, `flight_search.py`, `flight_data.py`, `notification_manager.py`), and S03 wants a small repository ([SA-001] conflicts). The Python checklist (`QC-PY-001`) asks for the layer folders `domain`, `application`, `infrastructure` and `presentation`, for logging instead of `print`, and for a Design Class Diagram.

Options considered:

1. Full clean-architecture layout with a `logging` set-up and a DCD. Cleanest on paper, but it hides the assignment's names behind layers and adds about four packages for five small classes.
2. Keep the Day 39 flat package `src/flight_club/` with one module per assignment class, console output through `print`, no DCD. Small and recognisable; the layers are merged.
3. A middle way with `domain/` only. Splits the two data classes from the rest and still breaks the assignment's file names.

The forces: the program is a one-shot console script whose output *is* the user interface ("Print a message" in the assignment), has about 300 lines and five classes, and has one delivery mechanism.

## Decision

Keep option 2: one flat package with the assignment's module and class names. The modules still depend inward in practice (`constants` imports nothing and `flight_data` imports only `constants`; `main` is the composition root and the only module that wires them), console messages use `print` because they are the program's output, and the assignment's class list serves as the design instead of a separate DCD.

## Consequences

**Positive:**

- S02 finds the assignment's names; S03 sees a small repository with no extra packages.
- The Day 39 code and tests carry over without a restructuring.

**Negative:**

- The layers `domain`, `application`, `infrastructure` and `presentation` are merged; `QC-PY-001` criterion 17 is met only by this ADR.
- `print` is used for the program's output, so there is no log level or log file; secrets are kept out of the output by printing error types instead of error texts.
- If the program grows (a second delivery mechanism, a database), this decision must be revisited and the layers split.

## Affected Artifacts

- [BC-001] — keeps the Business Case scope of the assignment's classes and names.
- [SA-001] — resolves the conflict between S02 and S03 and the clean-architecture folders.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
