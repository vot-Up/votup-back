# PRD: Django Unfold Admin para Votup

## Overview
Add django-unfold as the sole admin interface for the Votup voting system, replacing the default Django admin. The project currently has zero model registrations in admin.py files — all 8 business models and the custom User model are invisible in the admin. This feature creates a fully configured, modern admin interface organized by domain, with inline relationships, custom actions, and advanced Unfold features, enabling visual verification that all data and relationships remain intact after the hexagonal-to-service-layer migration.

## Goals
- Every model in the system is visible, searchable, and editable from the admin
- Admin users can verify post-migration data integrity by browsing relationships inline
- Custom admin actions replicate key service-layer operations (activate/close voting, activate plate)
- Sidebar navigation organized by business domain for intuitive wayfinding
- Leverage Unfold advanced features (fieldset tabs, compressed fields, command palette, dark mode) for a polished internal tool

## User Stories

### Admin / Developer (primary persona)
- As an admin, I want to see all voters and their voting history in one page so that I can verify data integrity after the refactoring
- As an admin, I want to search candidates by name or cellphone so that I can quickly find specific records
- As an admin, I want to see plate members inline on the plate detail page so that I can verify president/vice-president associations
- As an admin, I want to activate or close a voting event directly from the admin so that I don't need to use the API for basic operations
- As an admin, I want to see voting results (ResumeVote) inline on the event detail page so that I can verify vote counts match expectations
- As an admin, I want to navigate the sidebar by domain (Votação, Pessoas, Chapas, Sistema) so that I can find what I need without scrolling through alphabetically ordered apps
- As an admin, I want dark mode support so that I can work comfortably in low-light environments
- As an admin, I want to use the command palette to jump to any model so that I can navigate quickly

### System User (secondary persona)
- As a system user, I want to manage User accounts, Groups, and Tokens from the admin so that I can control access

## Core Features

### F1: Unfold Installation & Configuration
- Install django-unfold, configure as sole admin interface
- Replace `django.contrib.admin` with Unfold's admin site in INSTALLED_APPS
- Configure `UNFOLD` settings dict with site title, header, and theme defaults
- Enable dark mode toggle, command palette, and UI warnings

### F2: Domain-Organized Sidebar
- 4 sidebar sections with icons:
  - **Votação** (icon: `how_to_vote`): EventVoting, VotingUser, VotingPlate, ResumeVote
  - **Pessoas** (icon: `people`): Voter, Candidate
  - **Chapas** (icon: `groups`): Plate, PlateUser
  - **Sistema** (icon: `settings`): User, Group, Token, FlatPage, Redirect

### F3: Model Registrations with Full Customization

#### Voter
- list_display: name, cellphone, avatar, active, created_at
- search_fields: name, cellphone
- list_filter: active
- compressed_fields: True

#### Candidate
- list_display: name, cellphone, avatar_url, disabled, active, created_at
- search_fields: name, cellphone
- list_filter: disabled, active
- list_display_links: name
- compressed_fields: True

#### Plate
- list_display: name, active, created_at
- search_fields: name
- list_filter: active
- inlines: PlateUserInline (tabular)
- compressed_fields: True

#### PlateUser
- list_display: plate, candidate, type, active
- list_filter: type, active
- search_fields: plate__name, candidate__name
- compressed_fields: True

#### EventVoting
- list_display: description, date, active, created_at
- search_fields: description
- list_filter: active
- inlines: VotingPlateInline, VotingUserInline, ResumeVoteInline
- actions: activate_voting, close_voting
- compressed_fields: True
- fieldset_tabs: group date/description vs status fields

#### VotingPlate
- list_display: voting, plate, active, created_at
- list_filter: active
- search_fields: voting__description, plate__name
- compressed_fields: True

#### VotingUser
- list_display: voting, voter, plate, active, created_at
- list_filter: active
- search_fields: voting__description, voter__name, plate__name
- compressed_fields: True

#### ResumeVote
- list_display: voting, plate, quantity, active, created_at
- list_filter: active
- search_fields: voting__description, plate__name
- compressed_fields: True

#### User (account)
- list_display: email, name, cellphone, is_staff, is_active, created_at
- search_fields: email, name, cellphone
- list_filter: is_staff, is_active
- compressed_fields: True
- fieldset_tabs: personal info vs permissions vs dates

### F4: Inline Relationships
- PlateUserInline on Plate (tabular, show candidate name + type)
- VotingPlateInline on EventVoting (tabular, show plate name)
- VotingUserInline on EventVoting (tabular, show voter name + plate name)
- ResumeVoteInline on EventVoting (tabular, show plate name + quantity)

### F5: Custom Admin Actions
- **Activate Voting**: sets EventVoting.active=True, activates associated plates (calls `voting_service.active_vote`)
- **Close Voting**: sets EventVoting.active=False, deactivates associated plates (calls `voting_service.close_vote`)
- **Activate Plate**: sets Plate.active=True (calls `plate_service.activate_plate`)

### F6: Advanced Unfold Features
- Command palette enabled for quick model navigation
- Dark mode toggle available in header
- Compressed fields on all ModelAdmins for space efficiency
- Fieldset tabs on EventVoting and User forms for organized field grouping
- warn_unsaved_form: True on all ModelAdmins

### F7: System Models Registration
- Group (standard Django admin)
- Token / TokenProxy (DRF authtoken)
- FlatPage (django.contrib.flatpages)
- Redirect (django.contrib.redirects)

## User Experience
1. Admin accesses `/admin/` and sees a modern Unfold interface with branded header
2. Sidebar shows 4 domain sections with icons; each expands to show related models
3. Clicking "EventVoting" shows a changelist with search bar and filters for active status
4. Clicking a specific event shows its details with tabbed inlines (VotingPlate, VotingUser, ResumeVote) in fieldset tabs
5. Admin can use the dropdown action menu to "Activate" or "Close" a voting event directly
6. Command palette (Cmd+K) allows jumping to any model instantly
7. Dark mode toggle in the top-right corner for comfort

## High-Level Technical Constraints
- Must work with Django 5.2+ and Python 3.12+ (current project versions)
- Must not interfere with existing REST API endpoints or service layer
- Admin actions must use existing service layer functions (not duplicate logic)
- S3/MinIO storage for avatar ImageFields must be accessible from admin

## Non-Goals (Out of Scope)
- Custom dashboard with charts or statistics widgets (can be added later)
- Custom admin authentication flow (uses default Django admin login)
- API endpoint management from admin
- Import/export functionality for bulk data operations
- Audit logging or version history for admin changes
- Mobile-optimized admin layout (Unfold is responsive but not specifically optimized for mobile)

## Phased Rollout Plan

### MVP (Phase 1)
- Install and configure django-unfold
- Register all 8 business models + User with basic list_display, search_fields, list_filter
- Configure sidebar with 4 domain sections
- Add inlines for key relationships (PlateUser on Plate, VotingPlate/VotingUser/ResumeVote on EventVoting)
- Add custom actions (activate/close voting, activate plate)
- Register system models (Group, Token, FlatPage, Redirect)
- Success criteria: all models visible and editable in admin, no errors on `manage.py check`, all existing tests still pass

### Phase 2 (Future)
- Fieldset tabs on complex forms
- Compressed fields optimization
- Command palette and dark mode fine-tuning
- Custom dashboard with vote statistics
- Success criteria: admin feels polished and production-ready

## Success Metrics
- All 8 business models + User + 4 system models are registered and accessible in admin
- Every model changelist has functional search and filters
- Inline relationships display correctly on parent model detail pages
- Custom admin actions execute without errors and produce correct state changes
- `uv run python manage.py check` passes with zero issues
- `uv run pytest` passes with all existing tests green
- Admin loads in under 3 seconds on local development

## Risks and Mitigations
- **Unfold version compatibility**: django-unfold v0.93.0 requires Django >=5.1 — project uses Django 5.2, so compatible. Mitigated by pinning version in pyproject.toml
- **Avatar image display**: ImageFields use S3/MinIO storage — if MinIO is not running, avatars won't render. Mitigated by documenting that MinIO must be running for full admin experience
- **Admin action side effects**: Custom actions modify data via service layer — if service layer has bugs, admin actions will expose them. Mitigated by the fact that this is the exact purpose (verification)
- **Over-customization maintenance**: Heavily customized ModelAdmins may need updates when models change. Mitigated by models being stable in this project

## Architecture Decision Records
- [ADR-001: Setup Completo com Funcionalidades Avançadas](adrs/adr-001.md) — Unfold as sole admin with full customization, sidebar by domain, and advanced features from the start

## Open Questions
- Should the admin enforce the same business rules as the API (e.g., preventing duplicate votes, validating plate uniqueness)? Or should it allow raw data editing for verification purposes?
- Should Unfold's `SHOW_HISTORY` be enabled to leverage django-reversion for audit trail?
