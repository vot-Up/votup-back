# TechSpec: Django Unfold Admin para Votup

## Executive Summary
Replace the default Django admin with django-unfold as the sole admin interface. Register all 8 business models (Voter, Candidate, Plate, PlateUser, EventVoting, VotingPlate, VotingUser, ResumeVote) plus the custom User model with full customization: list displays, search, filters, inline relationships, and custom actions that delegate to the service layer. Organize the admin code as a Python module (`core/admin/`) with domain-specific files matching the 4-section sidebar (Votação, Pessoas, Chapas, Sistema). Replace django-reversion with django-simple-history for native Unfold version history support. The primary trade-off is exchanging django-reversion (already installed, no Unfold styling) for django-simple-history (new dependency, native Unfold integration) to get properly styled history pages.

## System Architecture

### Component Overview
- **Unfold Configuration** (`votup/settings.py`): INSTALLED_APPS, UNFOLD dict, simple-history settings
- **Core Admin Module** (`core/admin/`): `__init__.py`, `voting.py`, `people.py`, `plates.py` — ModelAdmins, Inlines, Actions
- **Account Admin** (`account/admin.py`): UserAdmin with Unfold base class
- **Service Layer Integration**: Admin actions call `voting_service.active_vote()`, `voting_service.close_vote()`, `plate_service.activate_plate()` with error handling
- **URL Configuration** (`votup/urls.py`): Unfold admin site replaces default at `/admin/`

### Data Flow
```
Admin Action (UI) → ModelAdmin.action_method → try/except service_call → 
  success: message_user(INFO) + log
  failure: message_user(ERROR) + log
```

## Implementation Design

### Core Interfaces

```python
# core/admin/__init__.py — Re-exports all admin classes for autodiscovery
from core.admin.voting import *   # EventVotingAdmin, VotingPlateAdmin, VotingUserAdmin, ResumeVoteAdmin
from core.admin.people import *   # VoterAdmin, CandidateAdmin
from core.admin.plates import *   # PlateAdmin, PlateUserAdmin
```

```python
# Base admin class with shared Unfold configuration
from unfold.admin import ModelAdmin

class BaseVotupAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
```

### Data Models

No new database models. Add `HistoricalRecords` to existing business models for version tracking:

```python
# Addition to each business model in core/models/models.py
from simple_history.models import HistoricalRecords

class Voter(account_models.ModelBase):
    # ... existing fields ...
    history = HistoricalRecords()
```

Models to add `HistoricalRecords`: Voter, Candidate, Plate, PlateUser, EventVoting, VotingPlate, VotingUser, ResumeVote.

### Admin Registrations

#### core/admin/people.py — Voter, Candidate

```python
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from core.models.models import Voter, Candidate

@admin.register(Voter)
class VoterAdmin(ModelAdmin):
    list_display = ("name", "cellphone", "active", "created_at")
    search_fields = ("name", "cellphone")
    list_filter = ("active",)
    compressed_fields = True
    warn_unsaved_form = True
```

#### core/admin/plates.py — Plate, PlateUser, PlateUserInline

```python
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from core.models.models import Plate, PlateUser

class PlateUserInline(TabularInline):
    model = PlateUser
    tab = True

@admin.register(Plate)
class PlateAdmin(ModelAdmin):
    list_display = ("name", "active", "created_at")
    search_fields = ("name",)
    list_filter = ("active",)
    inlines = [PlateUserInline]
    actions = ["activate_plate_action"]
    compressed_fields = True
    warn_unsaved_form = True
```

#### core/admin/voting.py — EventVoting, VotingPlate, VotingUser, ResumeVote + Inlines + Actions

```python
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
import logging
from unfold.admin import ModelAdmin, TabularInline

from core.models.models import EventVoting, VotingPlate, VotingUser, ResumeVote
from core.services import voting_service, plate_service

logger = logging.getLogger(__name__)

class VotingPlateInline(TabularInline):
    model = VotingPlate
    tab = True

class VotingUserInline(TabularInline):
    model = VotingUser
    tab = True

class ResumeVoteInline(TabularInline):
    model = ResumeVote
    tab = True

@admin.register(EventVoting)
class EventVotingAdmin(ModelAdmin):
    list_display = ("description", "date", "active", "created_at")
    search_fields = ("description",)
    list_filter = ("active",)
    inlines = [VotingPlateInline, VotingUserInline, ResumeVoteInline]
    actions = ["activate_voting", "close_voting"]
    compressed_fields = True
    warn_unsaved_form = True
    
    def activate_voting(self, request, queryset):
        for event in queryset:
            try:
                voting_service.active_vote(event.id)
                self.message_user(request, f"Votação '{event.description}' ativada.")
            except Exception as e:
                logger.error(f"Erro ao ativar votação {event.id}: {e}")
                self.message_user(request, str(e), level=messages.ERROR)
    activate_voting.short_description = "Ativar votação selecionada"
    
    def close_voting(self, request, queryset):
        for event in queryset:
            try:
                voting_service.close_vote(event.id)
                self.message_user(request, f"Votação '{event.description}' encerrada.")
            except Exception as e:
                logger.error(f"Erro ao encerrar votação {event.id}: {e}")
                self.message_user(request, str(e), level=messages.ERROR)
    close_voting.short_description = "Encerrar votação selecionada"
```

#### account/admin.py — User

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from account.models import User

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("email", "name", "cellphone", "is_staff", "is_active", "created_at")
    search_fields = ("email", "name", "cellphone")
    list_filter = ("is_staff", "is_active")
    compressed_fields = True
    warn_unsaved_form = True
```

### Sidebar Configuration

```python
# votup/settings.py — UNFOLD dict (sidebar section)
UNFOLD = {
    "SITE_TITLE": "Votup Admin",
    "SITE_HEADER": "Votup",
    "SITE_SYMBOL": "how_to_vote",
    "SHOW_HISTORY": True,
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "navigation": [
            {
                "title": _("Votação"),
                "icon": "how_to_vote",
                "collapsible": True,
                "items": [
                    {"title": _("Eventos de Votação"), "icon": "event", "link": "/admin/core/eventvoting/"},
                    {"title": _("Votos"), "icon": "how_to_reg", "link": "/admin/core/votinguser/"},
                    {"title": _("Chapas na Votação"), "icon": "ballot", "link": "/admin/core/votingplate/"},
                    {"title": _("Resumo de Votos"), "icon": "bar_chart", "link": "/admin/core/resumevote/"},
                ],
            },
            {
                "title": _("Pessoas"),
                "icon": "people",
                "collapsible": True,
                "items": [
                    {"title": _("Eleitores"), "icon": "person", "link": "/admin/core/voter/"},
                    {"title": _("Candidatos"), "icon": "badge", "link": "/admin/core/candidate/"},
                ],
            },
            {
                "title": _("Chapas"),
                "icon": "groups",
                "collapsible": True,
                "items": [
                    {"title": _("Chapas"), "icon": "group", "link": "/admin/core/plate/"},
                    {"title": _("Membros de Chapas"), "icon": "person_add", "link": "/admin/core/plateuser/"},
                ],
            },
            {
                "title": _("Sistema"),
                "icon": "settings",
                "collapsible": True,
                "items": [
                    {"title": _("Usuários"), "icon": "manage_accounts", "link": "/admin/account/user/"},
                    {"title": _("Grupos"), "icon": "admin_panel_settings", "link": "/admin/auth/group/"},
                    {"title": _("Tokens"), "icon": "key", "link": "/admin/authtoken/tokenproxy/"},
                ],
            },
        ],
    },
}
```

## Integration Points

### S3/MinIO Storage
- ImageFields (Voter.avatar, Candidate.avatar_url, User.avatar) use `S3Boto3Storage` via `DEFAULT_FILE_STORAGE`
- Admin will display S3 URLs for images — MinIO must be running for images to render
- No configuration change needed — Unfold inherits Django's storage backend

### Service Layer
- Admin actions call `voting_service.active_vote()`, `voting_service.close_vote()`, `plate_service.activate_plate()`
- Services may raise `DoesNotExist`, `ValidationError`, or other exceptions
- All exceptions caught with try/except, logged, and shown via `message_user`

## Impact Analysis

| Component | Impact Type | Description and Risk | Required Action |
|-----------|-------------|---------------------|-----------------|
| `votup/settings.py` | modified | Add unfold, simple_history, unfold.contrib to INSTALLED_APPS; add UNFOLD dict | Low risk — additive change |
| `votup/urls.py` | modified | Replace `from django.contrib import admin` with Unfold admin site | Low risk — URL path unchanged |
| `core/admin.py` | deleted | Remove empty file | No risk — empty file |
| `core/admin/` | new | Module with __init__.py, voting.py, people.py, plates.py | New code, medium effort |
| `account/admin.py` | modified | Register User with Unfold ModelAdmin | Low risk — single model |
| `core/models/models.py` | modified | Add `history = HistoricalRecords()` to 8 models | Medium risk — creates migration |
| `account/models.py` | modified | Add `history = HistoricalRecords()` to User model | Low risk — creates migration |
| `core/viewset.py` | modified | Remove `from reversion import revisions` import | Low risk — verify reversion not used elsewhere |
| `pyproject.toml` | modified | Add django-unfold, django-simple-history; remove django-reversion | Low risk — dependency swap |
| Existing tests | none | No test changes needed — admin is UI-only | No risk |

## Testing Approach

### Unit Tests
- Test admin actions: mock service calls, verify `message_user` called with correct level on success and error
- Test admin registration: verify each model has a registered ModelAdmin
- Test sidebar configuration: verify UNFOLD dict structure

### Integration Tests
- `manage.py check` passes with zero issues after all changes
- `manage.py migrate` creates history tables without errors
- All existing 36 tests still pass
- Admin URLs respond with 200 (manual verification)

### Manual Verification
- Login to `/admin/` with superuser credentials
- Verify sidebar shows 4 sections with correct models
- Verify each model changelist loads with search and filters
- Verify inlines display on Plate and EventVoting detail pages
- Verify custom actions (activate/close voting, activate plate) work
- Verify dark mode toggle works
- Verify command palette (Cmd+K) works
- Verify history tab shows on model detail pages

## Development Sequencing

### Build Order
1. **Install dependencies** — add django-unfold, django-simple-history; remove django-reversion; run `uv sync` (no dependencies)
2. **Configure settings** — update INSTALLED_APPS, add UNFOLD dict, add simple_history settings (depends on step 1)
3. **Update urls.py** — replace Django admin with Unfold admin site (depends on step 2)
4. **Remove reversion import** — clean up `core/viewset.py` (depends on step 1)
5. **Add HistoricalRecords to models** — add `history` field to all 9 models, run migrations (depends on step 1)
6. **Create core/admin/ module** — `__init__.py`, `people.py`, `plates.py`, `voting.py` with all ModelAdmins, inlines, actions (depends on steps 2, 5)
7. **Update account/admin.py** — register User with Unfold ModelAdmin (depends on step 2)
8. **Run validation** — `manage.py check`, `manage.py migrate`, `pytest` (depends on all steps)

### Technical Dependencies
- django-unfold must be installed before settings changes (import fails otherwise)
- django-simple-history must be installed before model changes (HistoricalRecords import)
- Migrations must be created and run after model changes
- Admin module depends on service layer (already complete)

## Monitoring and Observability
- Admin actions log errors via `logging.getLogger(__name__)` at ERROR level
- Django admin log entries track all model changes (built-in)
- simple-history records provide full audit trail with user, timestamp, and change diff

## Technical Considerations

### Key Decisions
- **Decision**: Replace reversion with simple-history
  - **Rationale**: Unfold has native simple-history integration; reversion PR was rejected
  - **Trade-offs**: Loses existing reversion version data (if any); gains styled history UI
  - **Alternatives rejected**: Keeping reversion (unstyled history pages), no history (loses audit capability)

- **Decision**: Module-based admin organization (`core/admin/`)
  - **Rationale**: 8+ ModelAdmins don't fit in a single file; code mirrors sidebar domain structure
  - **Trade-offs**: Deviates from Django's single-file convention; better maintainability
  - **Alternatives rejected**: Single admin.py (too large), separate apps per domain (over-engineering)

- **Decision**: Actions call service layer directly
  - **Rationale**: Verification of service layer is the feature's purpose
  - **Trade-offs**: Admin constrained by same business rules as API; no bypass capability
  - **Alternatives rejected**: Bypass service (defeats verification purpose), hybrid (over-complex)

### Known Risks
- **simple-history migration on existing data**: Adding HistoricalRecords to models with existing rows creates empty initial history records. Mitigated by `simple_history` handling this gracefully — existing rows get no history entry, only future changes are tracked.
- **Unfold version compatibility**: Unfold v0.93.0 is pre-1.0; breaking changes possible. Mitigated by `>=0.93.0` constraint and test suite.
- **Sidebar hard-coded links**: Using hard-coded `/admin/...` paths in sidebar config. Mitigated by using `reverse_lazy()` for proper URL resolution.

## Architecture Decision Records
- [ADR-001: Setup Completo com Funcionalidades Avançadas](adrs/adr-001.md) — Unfold as sole admin with full customization from the start
- [ADR-002: Module-Based Admin Organization](adrs/adr-002.md) — `core/admin/` package with domain-specific files
- [ADR-003: Service Layer for Admin Actions with Error Handling](adrs/adr-003.md) — Actions call services, errors displayed via message_user + logging
- [ADR-004: Version History with django-simple-history](adrs/adr-004.md) — Replace reversion with simple-history for native Unfold integration
- [ADR-005: Unfold Version and Dependency Strategy](adrs/adr-005.md) — `django-unfold>=0.93.0` with minor updates allowed
