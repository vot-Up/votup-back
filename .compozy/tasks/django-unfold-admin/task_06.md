---
status: completed
title: Final validation and manual verification
type: test
complexity: low
dependencies:
- task_04
- task_05
---

# Task 06: Final validation and manual verification

## Overview
Run comprehensive validation after all admin implementation tasks are complete. Execute automated checks (`manage.py check`, pytest) and a manual verification checklist to confirm the Unfold admin is fully functional with all models registered, sidebar organized, inlines displaying, and actions working.

<critical>
- ALWAYS READ the PRD and TechSpec before starting
- REFERENCE TECHSPEC for implementation details — do not duplicate here
- FOCUS ON "WHAT" — describe what needs to be accomplished, not how
- MINIMIZE CODE — show code only to illustrate current structure or problem areas
- TESTS REQUIRED — every task MUST include tests in deliverables
</critical>

<requirements>
- MUST run `uv run python manage.py check` with zero issues
- MUST run `uv run pytest` with all existing tests passing
- MUST verify all 13 models are registered in admin (8 core + User + Group + TokenProxy + historical models discoverable)
- MUST verify sidebar displays 4 domain sections: Votação, Pessoas, Chapas, Sistema
- MUST verify all ModelAdmins have list_display, search_fields, and list_filter configured
- MUST verify inlines display on Plate and EventVoting detail pages
- MUST verify custom actions (activate_voting, close_voting, activate_plate) are available
- MUST verify dark mode toggle works in admin header
- MUST verify command palette is accessible
- MUST verify history tab appears on model detail pages (simple-history integration)
- MUST update MEMORY.md with final state
</requirements>

## Subtasks
- [x] 6.1 Run `manage.py check` and `pytest` — confirm zero issues and all tests pass
- [x] 6.2 Verify admin sidebar shows 4 domain sections with correct models
- [x] 6.3 Verify each model changelist has functional search and filters
- [x] 6.4 Verify inlines render on Plate and EventVoting detail pages
- [x] 6.5 Verify custom actions appear in action dropdowns
- [x] 6.6 Verify dark mode toggle and command palette work
- [x] 6.7 Verify history tab shows on model detail pages
- [x] 6.8 Write integration test that verifies all ModelAdmins are registered
- [x] 6.9 Update MEMORY.md with completion status

## Implementation Details
Manual verification requires running the development server (`uv run python manage.py runserver`) and logging into `/admin/` with superuser credentials. The integration test should programmatically verify that all expected models have registered ModelAdmins by checking `admin.site._registry`.

### Relevant Files
- `votup/settings.py` — UNFOLD configuration
- `core/admin/__init__.py` — all admin registrations
- `account/admin.py` — User admin registration
- `.compozy/tasks/django-unfold-admin/memory/MEMORY.md` — to be updated

### Dependent Files
- All admin files from tasks 01-05

### Related ADRs
- All ADRs (001-005) are validated in this task

## Deliverables
- Integration test verifying all 12+ ModelAdmins are registered
- Manual verification checklist completed (documented in task file or memory)
- `manage.py check` passes
- All pytest tests pass
- Updated MEMORY.md

## Tests
- Unit tests:
  - [ ] All 8 core models have registered ModelAdmins in admin.site._registry
  - [ ] User model has a registered ModelAdmin
  - [ ] Total registered model count >= 12 (core + account + auth + authtoken)
- Integration tests:
  - [ ] `manage.py check` passes with zero issues
  - [ ] `pytest` passes with all existing + new tests green
  - [ ] Admin index page returns 200 status code
- Test coverage target: >=80%

## Success Criteria
- All tests passing
- Test coverage >=80%
- `manage.py check` passes
- All existing 36+ tests pass
- All 4 sidebar sections visible
- All model changelists load with search and filters
- Inlines display on Plate and EventVoting detail pages
- Custom actions available in dropdown menus
- Dark mode toggle functional
- Command palette accessible
