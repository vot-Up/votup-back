# Task Memory: task_01.md

Keep only task-local execution context here. Do not duplicate facts that are obvious from the repository, task file, PRD documents, or git history.

## Objective Snapshot
- Inventariar toda arquitetura hexagonal antes da refatoração
- Nenhum código alterado — apenas análise estática e documentação

## Important Decisions
- Decisão de inventariar todos os imports, incluindo init__.py vazios
- Decisão de classificar por: "usado em viewset", "usado externamente", "candidato à remoção"

## Learnings
- `account/viewset.py` importa `core.schemas.schemas` (AUTH_SCHEMAS, USER_SCHEMAS) — única referência externa a hexagonais
- `core/adapters/storage/file_storage_adapter.py` é importado no viewset (S3FileStorageAdapter), não só internal
- `core/dto/voter_dto.py` é usado em VoterViewSet.can_vote — não é candidato imediato à remoção
- `core/domain/` é totalmente alcançável só via ports/repositories — nenhum import direto no viewset

## Files / Surfaces
- `inventory.md` criado em `.compozy/tasks/votup-rest-refactor/`

## Errors / Corrections
- Nenhum erro durante inventário

## Ready for Next Run
