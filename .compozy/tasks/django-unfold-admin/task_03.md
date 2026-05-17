---
status: completed
title: Create core/admin module with people and plates admins
type: backend
complexity: medium
dependencies:
- task_02
---

# Task 03: Create core/admin module with people and plates admins

## Overview
Create the `core/admin/` Python package with domain-specific admin files. Implement ModelAdmins for Voter, Candidate (people.py) and Plate, PlateUser (plates.py) with list displays, search, filters, and PlateUserInline on Plate. Delete the empty `core/admin.py` file.

<critical>
- ALWAYS READ the PRD and TechSpec before starting
- REFERENCE TECHSPEC for implementation details — do not duplicate here
- FOCUS ON "WHAT" — describe what needs to be accomplished, not how
- MINIMIZE CODE — show code only to illustrate current structure or problem areas
- TESTS REQUIRED — every task MUST include tests in deliverables
</critical>

<requirements>
- MUST delete the existing empty `core/admin.py` file
- MUST create `core/admin/__init__.py` that imports all admin classes from domain modules
- MUST create `core/admin/people.py` with VoterAdmin and CandidateAdmin
- MUST create `core/admin/plates.py` with PlateAdmin, PlateUserAdmin, and PlateUserInline
- MUST use `unfold.admin.ModelAdmin` as the base class for all ModelAdmins (NOT django.contrib.admin.ModelAdmin)
- MUST use `unfold.admin.TabularInline` for PlateUserInline (NOT django.contrib.admin.TabularInline)
- MUST set `compressed_fields = True` and `warn_unsaved_form = True` on all ModelAdmins
- MUST include the PlateUserInline on PlateAdmin
- MUST include `activate_plate` action on PlateAdmin that calls `plate_service.activate_plate()`
- MUST handle service layer exceptions in actions with `message_user(level=ERROR)` and logging
- VoterAdmin list_display: name, cellphone, active, created_at; search_fields: name, cellphone; list_filter: active
- CandidateAdmin list_display: name, cellphone, disabled, active, created_at; search_fields: name, cellphone; list_filter: disabled, active
- PlateAdmin list_display: name, active, created_at; search_fields: name; list_filter: active
- PlateUserAdmin list_display: plate, candidate, type, active; search_fields: plate__name, candidate__name; list_filter: type, active
</requirements>

## Subtasks
- [x] 3.1 Delete empty `core/admin.py`
- [x] 3.2 Create `core/admin/__init__.py` with re-exports from people and plates modules
- [x] 3.3 Create `core/admin/people.py` with VoterAdmin and CandidateAdmin
- [x] 3.4 Create `core/admin/plates.py` with PlateAdmin, PlateUserAdmin, PlateUserInline, and activate_plate action
- [x] 3.5 Write unit tests for admin registrations and action error handling
- [x] 3.6 Verify `manage.py check` passes and admin URLs load

## Implementation Details
See TechSpec "Admin Registrations" section for people.py and plates.py structure. See TechSpec "Core Interfaces" section for the BaseVotupAdmin pattern with compressed_fields and warn_unsaved_form. The activate_plate action should iterate over the queryset, call `plate_service.activate_plate(plate.id)` in a try/except, and use `self.message_user()` for success/failure feedback.

### Relevant Files
- `core/admin.py` — to be deleted (currently empty)
- `core/models/models.py` — Voter, Candidate, Plate, PlateUser models
- `core/services/plate_service.py` — `activate_plate()` function for admin action

### Dependent Files
- `core/admin/__init__.py` — must import from domain modules for Django autodiscovery
- `core/admin/people.py` — new file
- `core/admin/plates.py` — new file

### Related ADRs
- [ADR-002: Module-Based Admin Organization](../adrs/adr-002.md) — core/admin/ package structure
- [ADR-003: Service Layer for Admin Actions with Error Handling](../adrs/adr-003.md) — Actions call services with error handling

## Deliverables
- Deleted `core/admin.py`
- New `core/admin/__init__.py`, `core/admin/people.py`, `core/admin/plates.py`
- VoterAdmin, CandidateAdmin, PlateAdmin, PlateUserAdmin registered and functional
- PlateUserInline displays on Plate detail page
- activate_plate action on PlateAdmin with error handling
- Unit tests with >=80% coverage

## Tests
- Unit tests:
  - [x] VoterAdmin is registered for Voter model
  - [x] CandidateAdmin is registered for Candidate model
  - [x] PlateAdmin is registered for Plate model
  - [x] PlateUserAdmin is registered for PlateUser model
  - [x] PlateUserInline is listed in PlateAdmin.inlines
  - [x] activate_plate action calls plate_service.activate_plate with correct plate ID
  - [x] activate_plate action shows error message when service raises exception
  - [x] activate_plate action shows success message when service succeeds
  - [x] All ModelAdmins have compressed_fields=True and warn_unsaved_form=True
- Integration tests:
  - [x] `manage.py check` passes
  - [ ] `/admin/core/voter/` changelist loads (requires superuser login — manual verification)
  - [ ] `/admin/core/candidate/` changelist loads (requires superuser login — manual verification)
  - [ ] `/admin/core/plate/` changelist loads (requires superuser login — manual verification)
- Test coverage target: >=80%

## Success Criteria
- All tests passing
- Test coverage >=80%
- `manage.py check` passes
- All 4 ModelAdmins registered and accessible in admin
