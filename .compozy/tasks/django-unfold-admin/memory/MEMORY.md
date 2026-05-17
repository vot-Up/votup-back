# Workflow Memory

Keep only durable, cross-task context here. Do not duplicate facts that are obvious from the repository, PRD documents, or git history.

## Current State

- Task 01 complete: dependencies, INSTALLED_APPS, UNFOLD dict, and unit tests all verified and passing.
- Task 02 complete: HistoricalRecords added to all 9 models (8 business + User), migrations created and applied, 65 tests passing.
- Task 03 complete: core/admin/ module created with VoterAdmin, CandidateAdmin, PlateAdmin, PlateUserAdmin, PlateUserInline, and activate_plate_action. 110 tests passing.
- Task 04 is next: voting admin with inlines and actions.

## Shared Decisions

- Sidebar uses `reverse_lazy()` for all admin changelist links — not hard-coded paths.
- `simple_history.middleware.HistoryRequestMiddleware` must be in MIDDLEWARE for user tracking to work.
- django-reversion is fully removed from pyproject.toml (no entry present).
- Data migrations must use `apps.get_model()`, never direct model imports — direct imports trigger simple-history signals before history tables exist.

## Shared Learnings

- ruff I001 (import sorting) must be satisfied: all third-party imports must be in a single block without internal blank lines separating packages.
- The overall project coverage baseline is ~19% since most service files have no tests; task-specific test coverage is 100%.
- `HistoricalRecords` registers as `HistoryDescriptor` in model `__dict__`. Test with `isinstance(Model.__dict__['history'], HistoryDescriptor)` from `simple_history.manager`.

## Open Risks

- None from tasks 01–03. Task 04 needs to implement voting admin (EventVotingAdmin, VotingPlateAdmin, VotingUserAdmin, ResumeVoteAdmin) with activate_voting and close_voting actions.

## Handoffs

- History tables are present in the DB; migrations are clean (`makemigrations --check` returns no changes).
- 110 tests pass as of task_03 completion.
- action method name is `activate_plate_action` (not `activate_plate`) — registered via `actions = ["activate_plate_action"]`.
