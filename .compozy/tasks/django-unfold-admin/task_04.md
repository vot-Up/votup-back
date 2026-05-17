---
status: pending
title: Create voting admin with inlines and actions
type: backend
complexity: high
dependencies:
- task_03
---

# Task 04: Create voting admin with inlines and actions

## Overview
Create `core/admin/voting.py` with ModelAdmins for EventVoting, VotingPlate, VotingUser, and ResumeVote. Implement 3 tabular inlines on EventVoting (VotingPlateInline, VotingUserInline, ResumeVoteInline) and 2 custom admin actions (activate_voting, close_voting) that delegate to the voting service layer with error handling and logging.

<critical>
- ALWAYS READ the PRD and TechSpec before starting
- REFERENCE TECHSPEC for implementation details — do not duplicate here
- FOCUS ON "WHAT" — describe what needs to be accomplished, not how
- MINIMIZE CODE — show code only to illustrate current structure or problem areas
- TESTS REQUIRED — every task MUST include tests in deliverables
</critical>

<requirements>
- MUST create `core/admin/voting.py` with EventVotingAdmin, VotingPlateAdmin, VotingUserAdmin, ResumeVoteAdmin
- MUST update `core/admin/__init__.py` to import from voting module
- MUST use `unfold.admin.ModelAdmin` and `unfold.admin.TabularInline` as base classes
- MUST set `compressed_fields = True` and `warn_unsaved_form = True` on all ModelAdmins
- MUST create VotingPlateInline, VotingUserInline, ResumeVoteInline as TabularInline classes
- MUST attach all 3 inlines to EventVotingAdmin
- MUST set `tab = True` on all 3 inlines for Unfold tab grouping
- MUST implement `activate_voting` action on EventVotingAdmin that calls `voting_service.active_vote(event.id)`
- MUST implement `close_voting` action on EventVotingAdmin that calls `voting_service.close_vote(event.id)`
- MUST handle exceptions in both actions with `self.message_user(level=ERROR)` and `logging.getLogger(__name__)`
- EventVotingAdmin list_display: description, date, active, created_at; search_fields: description; list_filter: active
- VotingPlateAdmin list_display: voting, plate, active, created_at; search_fields: voting__description, plate__name; list_filter: active
- VotingUserAdmin list_display: voting, voter, plate, active, created_at; search_fields: voting__description, voter__name, plate__name; list_filter: active
- ResumeVoteAdmin list_display: voting, plate, quantity, active, created_at; search_fields: voting__description, plate__name; list_filter: active
</requirements>

## Subtasks
- [ ] 4.1 Create `core/admin/voting.py` with all 4 ModelAdmins and 3 Inlines
- [ ] 4.2 Implement activate_voting action with service call, error handling, and logging
- [ ] 4.3 Implement close_voting action with service call, error handling, and logging
- [ ] 4.4 Update `core/admin/__init__.py` to import voting module
- [ ] 4.5 Write unit tests for admin registrations and action behavior
- [ ] 4.6 Verify admin loads with inlines on EventVoting detail page

## Implementation Details
See TechSpec "Admin Registrations > core/admin/voting.py" section for the full structure. See TechSpec "Service Layer Integration" for the action error-handling pattern. Actions iterate over the queryset, call service functions per object, and report success/failure individually via `message_user`. Each inline uses `tab = True` for Unfold's inline tab grouping on the EventVoting change form.

### Relevant Files
- `core/admin/voting.py` — new file (all voting admin classes)
- `core/admin/__init__.py` — add voting module imports
- `core/models/models.py` — EventVoting, VotingPlate, VotingUser, ResumeVote models
- `core/services/voting_service.py` — `active_vote()`, `close_vote()` functions

### Dependent Files
- `core/admin/people.py` — already created in task_03, __init__.py must import from all domain modules
- `core/admin/plates.py` — already created in task_03

### Related ADRs
- [ADR-002: Module-Based Admin Organization](../adrs/adr-002.md) — voting.py as domain module
- [ADR-003: Service Layer for Admin Actions with Error Handling](../adrs/adr-003.md) — Actions with error handling pattern

## Deliverables
- New `core/admin/voting.py` with 4 ModelAdmins, 3 Inlines, 2 Actions
- Updated `core/admin/__init__.py` with voting imports
- activate_voting and close_voting actions functional with error handling
- Inlines display on EventVoting detail page
- Unit tests with >=80% coverage

## Tests
- Unit tests:
  - [ ] EventVotingAdmin is registered for EventVoting model
  - [ ] VotingPlateAdmin is registered for VotingPlate model
  - [ ] VotingUserAdmin is registered for VotingUser model
  - [ ] ResumeVoteAdmin is registered for ResumeVote model
  - [ ] EventVotingAdmin.inlines contains VotingPlateInline, VotingUserInline, ResumeVoteInline
  - [ ] activate_voting action calls voting_service.active_vote with correct event ID
  - [ ] activate_voting action shows success message when service succeeds
  - [ ] activate_voting action shows error message when service raises DoesNotExist
  - [ ] activate_voting action logs errors via logger
  - [ ] close_voting action calls voting_service.close_vote with correct event ID
  - [ ] close_voting action shows success message when service succeeds
  - [ ] close_voting action shows error message when service raises exception
  - [ ] All inlines have tab=True
  - [ ] All ModelAdmins have compressed_fields=True and warn_unsaved_form=True
- Integration tests:
  - [ ] `manage.py check` passes
  - [ ] `/admin/core/eventvoting/` changelist loads
  - [ ] EventVoting detail page shows inline tabs for plates, votes, and resume
- Test coverage target: >=80%

## Success Criteria
- All tests passing
- Test coverage >=80%
- `manage.py check` passes
- EventVotingAdmin displays with 3 inlines and 2 actions
