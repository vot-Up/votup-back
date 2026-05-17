# Task Memory: task_03.md

Keep only task-local execution context here. Do not duplicate facts that are obvious from the repository, task file, PRD documents, or git history.

## Objective Snapshot

Create core/admin/ Python package replacing the empty core/admin.py. Implement VoterAdmin, CandidateAdmin (people.py), PlateAdmin, PlateUserAdmin, PlateUserInline (plates.py) with unfold.admin base classes.

## Important Decisions

- Action method named `activate_plate_action` (matching techspec `actions = ["activate_plate_action"]`), not `activate_plate`.
- No BaseVotupAdmin class created — techspec shows it as a pattern; task does not require it and inline repetition is minimal.
- PlateUserInline uses `tab = True` per techspec pattern.

## Learnings

- Admin files need 100% coverage with class-attribute tests and action mock tests — fast and straightforward.
- `admin.site._registry.get(Model)` is the reliable way to assert admin registrations.

## Files / Surfaces

- Deleted: `core/admin.py`
- Created: `core/admin/__init__.py`, `core/admin/people.py`, `core/admin/plates.py`
- Created: `core/tests/test_core_admin.py` (29 tests, 100% admin coverage)

## Errors / Corrections

None.

## Ready for Next Run

Task complete. 110 tests pass. manage.py check clean. Diff ready for manual review/commit.
