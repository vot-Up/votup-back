---
status: pending
title: Configure account admin and system models
type: backend
complexity: low
dependencies:
- task_01
---

# Task 05: Configure account admin and system models

## Overview
Register the custom User model with an Unfold-based ModelAdmin in `account/admin.py`. Verify that system models (Group, TokenProxy) are accessible in the admin — they use Django's default admin registration and will be styled by Unfold automatically.

<critical>
- ALWAYS READ the PRD and TechSpec before starting
- REFERENCE TECHSPEC for implementation details — do not duplicate here
- FOCUS ON "WHAT" — describe what needs to be accomplished, not how
- MINIMIZE CODE — show code only to illustrate current structure or problem areas
- TESTS REQUIRED — every task MUST include tests in deliverables
</critical>

<requirements>
- MUST register the User model in `account/admin.py` with `unfold.admin.ModelAdmin` as base class
- MUST set `compressed_fields = True` and `warn_unsaved_form = True` on UserAdmin
- UserAdmin list_display: email, name, cellphone, is_staff, is_active, created_at
- UserAdmin search_fields: email, name, cellphone
- UserAdmin list_filter: is_staff, is_active
- MUST NOT register Group or TokenProxy manually — they are auto-registered by Django and DRF, and Unfold styles them automatically
- MUST verify that system models (Group, TokenProxy) appear in the admin sidebar under the "Sistema" section
</requirements>

## Subtasks
- [ ] 5.1 Create UserAdmin in `account/admin.py` with Unfold ModelAdmin base
- [ ] 5.2 Verify Group and TokenProxy are visible in admin (auto-registered)
- [ ] 5.3 Write unit tests for UserAdmin registration
- [ ] 5.4 Verify admin URLs for User, Group, and TokenProxy load correctly

## Implementation Details
See TechSpec "Admin Registrations > account/admin.py" section for UserAdmin structure. Group is auto-registered by `django.contrib.auth` and TokenProxy by `rest_framework.authtoken`. Unfold styles all registered models automatically — no manual registration needed for these. The sidebar "Sistema" section configured in task_01 provides direct links to these models.

### Relevant Files
- `account/admin.py` — currently empty, will contain UserAdmin
- `account/models.py` — User model

### Dependent Files
- `votup/settings.py` — UNFOLD sidebar configuration (from task_01) provides Sistema section links

### Related ADRs
- [ADR-001: Setup Completo com Funcionalidades Avançadas](../adrs/adr-001.md) — Unfold as sole admin

## Deliverables
- Updated `account/admin.py` with UserAdmin
- Unit tests for UserAdmin registration
- Verification that Group and TokenProxy are accessible in admin

## Tests
- Unit tests:
  - [ ] UserAdmin is registered for User model
  - [ ] UserAdmin has compressed_fields=True and warn_unsaved_form=True
  - [ ] UserAdmin list_display contains email, name, cellphone, is_staff, is_active
  - [ ] UserAdmin search_fields contains email, name, cellphone
- Integration tests:
  - [ ] `/admin/account/user/` changelist loads
  - [ ] `/admin/auth/group/` changelist loads
  - [ ] `/admin/authtoken/tokenproxy/` changelist loads
- Test coverage target: >=80%

## Success Criteria
- All tests passing
- Test coverage >=80%
- UserAdmin registered and accessible
- Group and TokenProxy visible in admin
