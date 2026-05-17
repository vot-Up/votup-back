# Task Memory: task_03.md

Keep only task-local execution context here. Do not duplicate facts that are obvious from the repository, task file, PRD documents, or git history.

## Objective Snapshot
- Migrar `UpdateCandidateAvatarUseCase` para `core/services/candidate_service.py`
- Atualizar `core/viewset.py` para usar `update_avatar()` do service
- Manter contrato HTTP de `PATCH /candidates/{id}/avatar/` intacto

## Important Decisions
- Usado `django.shortcuts.get_object_or_404` no service — padrão Django para busca por PK
- `S3FileStorageAdapter` instanciado diretamente dentro do service (sem Port intermediário)
- Endpoint retorna `204 No Content` — preserved from original

## Files / Surfaces
- **Criado:** `core/services/candidate_service.py` — função `update_avatar(candidate_id, file, filename)`
- **Modificado:** `core/viewset.py` — linha 33: import substituído; linha 134: chamada substituída
- **Lido (não modificado):** `core/use_cases/update_candidate_avatar_use_case.py`, `core/repositories/candidate_repository.py`, `core/adapters/storage/file_storage_adapter.py`, `core/ports/candidate_repository_port.py`, `core/ports/file_storage_port.py`
- **Referenciado:** `core/models/models.py` (modelo Candidate)

## Learnings
- `core/services/__init__.py` já tinha docstring indicando `candidate_service` como módulo futuro — criado durante task_02
- `CandidateRepository` usa `Candidate` domain entity (core/domain/candidate.py), não Django Model — service acessa ORM diretamente

## Errors / Corrections
- Nenhum erro durante implementação
- `manage.py check` passou com 0 issues
- `uv run pytest` coletou 0 testes (pré-existente, não é regressão)

## Ready for Next Run
- Pronto para cy-final-verify e atualização de tracking
