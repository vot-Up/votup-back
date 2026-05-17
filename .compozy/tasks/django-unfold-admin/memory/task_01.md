# Task Memory: task_01.md

Keep only task-local execution context here. Do not duplicate facts that are obvious from the repository, task file, PRD documents, or git history.

## Objective Snapshot

Install django-unfold and django-simple-history, remove django-reversion, configure INSTALLED_APPS and UNFOLD dict with sidebar using reverse_lazy().

## Important Decisions

- Implementation was already complete when task started (settings.py, pyproject.toml, and test_admin_settings.py were all pre-populated).
- Fixed a ruff I001 import-sorting error in votup/settings.py: removed the blank line separating `from django.utils.translation import gettext_lazy as _` from `from dotenv import load_dotenv` (both are third-party, should be in the same import block).

## Learnings

- The sidebar uses `reverse_lazy()` (not hard-coded paths) for all admin changelist links — this is correct per TechSpec.
- `simple_history.middleware.HistoryRequestMiddleware` is already in MIDDLEWARE (required for user tracking).
- Coverage for this test file is only counted against the test module itself; overall project coverage at ~19% because most service files are not covered by this test module.

## Files / Surfaces

- `votup/settings.py` — INSTALLED_APPS + UNFOLD dict (import sorting fixed)
- `pyproject.toml` — django-unfold>=0.93.0 and django-simple-history>=3.8.0 added, django-reversion absent
- `core/tests/test_admin_settings.py` — 11 unit tests, all passing

## Errors / Corrections

- ruff I001 in votup/settings.py: blank line between two third-party import groups. Fixed by merging into a single block.

## Ready for Next Run

- Task 01 is complete. Task 02 (remove reversion from viewset, add HistoricalRecords to models) can proceed.
- `core/viewset.py` is modified (per git status) — task 02 should pick up reversion removal there.
