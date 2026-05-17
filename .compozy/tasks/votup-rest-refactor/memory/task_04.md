# Task Memory: task_04.md

## Objective Snapshot
Migrar `ActivatePlateUseCase`, `DeleteUserPlateUseCase` e `DeleteVotingPlateUseCase` para `core/services/plate_service.py`.
Atualizar `core/viewset.py` para usar as novas funções de serviço, removendo imports dos use-cases.
Preservar contratos HTTP dos endpoints de chapa.

## Important Decisions
- `PlateRepository`, `PlateUserRepository`, `VotingPlateRepository` não são mais usadas pelos três use-cases migrados — o viewset acessa o ORM diretamente via `plate_service`.
- `VotingPlateRepository` (classe) ainda é usada no endpoint `check_associate` de `VotingPlateViewSet` via `CheckPlateAssociateUseCase` — NÃO removida nesta task.

## Learnings
- `PlateUserRepository` e `PlateRepository` (classes) não têm mais nenhuma referência no código após esta migração; propostas para remoção em task_08.
- `VotingPlateRepository` (classe) só é usada por `CheckPlateAssociateUseCase` — target de task_05.

## Files / Surfaces
- Criado: `core/services/plate_service.py`
- Modificado: `core/viewset.py`
- Informacional: `core/use_cases/activite_plate_use_case.py`, `core/use_cases/delete_plate_user_use_case.py`, `core/use_cases/delete_voting_plate_use_case.py` (não deletadas — preservar até task_08)

## Errors / Corrections
Nenhum erro encontrado. viewset.py já estava no estado correto.

## Ready for Next Run
Task concluída. Próxima: task_05 (associações).
