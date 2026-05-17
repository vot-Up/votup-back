# Workflow Memory
Keep only durable, cross-task context here. Do not duplicate facts that are obvious from the repository, PRD documents, or git history.

## Current State
- All 6 tasks COMPLETE. django-unfold-admin workflow finished.
- 215 tests passing, manage.py check clean, 69.8% overall coverage.
- Admin module coverage: 100% on all core/admin/ files and account/admin.py.

## Shared Decisions
- Sidebar uses `reverse_lazy()` for all admin changelist links — not hard-coded paths.
- `simple_history.middleware.HistoryRequestMiddleware` must be in MIDDLEWARE for user tracking.
- django-reversion fully removed from pyproject.toml and codebase.
- Data migrations must use `apps.get_model()`, never direct model imports — direct imports trigger simple-history signals before history tables exist.
- Total registered admin models = 11 (8 core + User + Group + TokenProxy).

## Shared Learnings
- ruff I001 (import sorting): all third-party imports must be in a single block without internal blank lines separating packages.
- The overall project coverage baseline is ~19% since most service files have no tests; task-specific admin coverage is 100%.
- `HistoricalRecords` registers as `HistoryDescriptor` in model `__dict__`. Test with `isinstance(Model.__dict__['history'], HistoryDescriptor)` from `simple_history.manager`.
- Pre-existing ruff D-rule failures exist in core/services/ files — these are out of scope for the admin workflow.
- action method name is `activate_plate_action` (not `activate_plate`) — registered via `actions = ["activate_plate_action"]`.
- User model requires `cellphone` field in `create_user()`.

## Open Risks
- None. All 6 tasks complete.

## Handoffs
- History tables present in DB; migrations clean (`makemigrations --check` returns no changes).
- Manual verification items (dark mode, command palette, history tab UI) require running dev server with superuser login — automated tests cover all registration and configuration.
- `account/tests/` directory has no `__init__.py` (matches `core/tests/` pattern) — required to avoid module name conflict with `account/tests.py`.
