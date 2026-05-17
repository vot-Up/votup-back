---
status: completed
title: Install dependencies and configure settings
type: backend
complexity: medium
dependencies: []
---

# Task 01: Install dependencies and configure settings

## Overview
Install django-unfold and django-simple-history, remove django-reversion from dependencies, and configure the project settings to enable Unfold as the sole admin interface with a domain-organized sidebar.

<critical>
- ALWAYS READ the PRD and TechSpec before starting
- REFERENCE TECHSPEC for implementation details — do not duplicate here
- FOCUS ON "WHAT" — describe what needs to be accomplished, not how
- MINIMIZE CODE — show code only to illustrate current structure or problem areas
- TESTS REQUIRED — every task MUST include tests in deliverables
</critical>

<requirements>
- MUST add `django-unfold>=0.93.0` to pyproject.toml dependencies
- MUST add `django-simple-history` to pyproject.toml dependencies
- MUST remove `django-reversion>=5.1.0` from pyproject.toml dependencies
- MUST add `"unfold"` as the FIRST entry in INSTALLED_APPS (before django.contrib.admin)
- MUST add `"unfold.contrib.filters"` and `"unfold.contrib.simple_history"` to INSTALLED_APPS
- MUST add `"simple_history"` to INSTALLED_APPS
- MUST keep `"django.contrib.admin"` in INSTALLED_APPS (required by Unfold)
- MUST add UNFOLD dict to settings.py with: SITE_TITLE, SITE_HEADER, SITE_SYMBOL, SHOW_HISTORY, SIDEBAR navigation
- MUST configure SIDEBAR with 4 domain sections: Votação, Pessoas, Chapas, Sistema
- MUST use `reverse_lazy()` for sidebar links (not hard-coded paths)
- MUST run `uv sync` after dependency changes
</requirements>

## Subtasks
- [x] 1.1 Add django-unfold and django-simple-history to pyproject.toml, remove django-reversion
- [x] 1.2 Run `uv sync` to install new dependencies
- [x] 1.3 Update INSTALLED_APPS in votup/settings.py with unfold, unfold.contrib, simple_history
- [x] 1.4 Add UNFOLD configuration dict with site branding and sidebar navigation
- [x] 1.5 Verify `uv run python manage.py check` passes

## Implementation Details
See TechSpec "Sidebar Configuration" section for the UNFOLD dict structure. See TechSpec "System Architecture" for INSTALLED_APPS ordering. The sidebar must use `reverse_lazy()` from `django.urls` for all admin changelist links.

### Relevant Files
- `votup/settings.py` — INSTALLED_APPS and new UNFOLD dict
- `pyproject.toml` — dependency changes

### Dependent Files
- `votup/urls.py` — will need admin site update in task_05 scope (Unfold replaces default admin site, but URL config remains compatible)

### Related ADRs
- [ADR-001: Setup Completo com Funcionalidades Avançadas](../adrs/adr-001.md) — Unfold as sole admin
- [ADR-004: Version History with django-simple-history](../adrs/adr-004.md) — Replace reversion with simple-history
- [ADR-005: Unfold Version and Dependency Strategy](../adrs/adr-005.md) — Version constraints

## Deliverables
- Updated pyproject.toml with new dependencies (unfold, simple-history) and reversion removed
- Updated votup/settings.py with INSTALLED_APPS changes and UNFOLD dict
- `uv sync` runs successfully
- `uv run python manage.py check` passes with zero issues
- Unit test verifying UNFOLD dict contains required keys (SITE_TITLE, SIDEBAR)

## Tests
- Unit tests:
  - [ ] UNFOLD settings dict exists and contains SITE_TITLE, SITE_HEADER, SITE_SYMBOL, SHOW_HISTORY
  - [ ] SIDEBAR navigation has exactly 4 sections with correct titles
  - [ ] "unfold" appears in INSTALLED_APPS before "django.contrib.admin"
  - [ ] "simple_history" appears in INSTALLED_APPS
  - [ ] "reversion" does NOT appear in INSTALLED_APPS
- Integration tests:
  - [ ] `manage.py check` passes with zero issues
- Test coverage target: >=80%

## Success Criteria
- All tests passing
- Test coverage >=80%
- `manage.py check` passes
- `uv sync` completes without errors
