# Task Memory: task_02.md

Keep only task-local execution context here. Do not duplicate facts that are obvious from the repository, task file, PRD documents, or git history.

## Objective Snapshot

Remove reversion from core/viewset.py and add HistoricalRecords to 8 business models + User model. Task complete.

## Important Decisions

- viewset.py was already clean of reversion at task start (cleaned in prior refactor commit).
- Used `apps.get_model()` in `account/migrations/0002_initial_user.py` to bypass HistoricalRecords signal during migration — direct `User` import caused ProgrammingError during test DB setup.

## Learnings

- `HistoricalRecords` registers as a `HistoryDescriptor` in the model's `__dict__`, not as `HistoricalRecords` itself. Test with `isinstance(Model.__dict__['history'], HistoryDescriptor)` from `simple_history.manager`.
- Data migrations that import model classes directly (not `apps.get_model`) trigger simple-history signals, which fail if history tables haven't been migrated yet.

## Files / Surfaces

- `core/models/models.py` — HistoricalRecords added to all 8 models
- `account/models.py` — HistoricalRecords added to User (not ModelBase)
- `account/migrations/0002_initial_user.py` — rewritten to use apps.get_model + make_password
- `account/migrations/0003_historicaluser.py` — new (generated)
- `core/migrations/0004_historicalcandidate_historicaleventvoting_and_more.py` — new (generated)
- `core/tests/test_history_and_viewset.py` — 18 new tests; all pass

## Errors / Corrections

- First run: `ProgrammingError: relation "account_historicaluser" does not exist` during test DB setup. Root cause: 0002_initial_user imported User directly, triggering history signal before 0003_historicaluser ran. Fixed by rewriting migration to use apps.get_model.

## Ready for Next Run

Task 03 (core/admin/ module with people and plates admins) can proceed. History tables are now present in the DB.
