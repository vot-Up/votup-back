---
status: completed
title: Migrar lógica de chapas/plates
type: refactor
complexity: medium
dependencies:
  - task_02
---

# Task 04: Migrar lógica de chapas/plates

## Overview
Mover `ActivatePlateUseCase`, `DeleteUserPlateUseCase` e `DeleteVotingPlateUseCase` para `core/services/plate_service.py`. Atualizar os imports no `core/viewset.py`. Todos os endpoints relacionados a chapas devem preservar seu contrato HTTP atual.

<critical>
- SEMPRE LER `core/use_cases/activite_plate_use_case.py`, `core/use_cases/delete_plate_user_use_case.py` e `core/use_cases/delete_voting_plate_use_case.py` antes de começar
- REFERÊNCIAR o inventário da task_01 para confirmar dependências
- FOCO NO "O QUÊ" — consolidar lógica de plates em um service
- MINIMIZAR CÓDIGO — manter lógica idêntica, sem novos comportamentos
- TESTES REQUERIDOS — todos os endpoints de chapa devem continuar funcionando
</critical>

<requirements>
- MUST criar `core/services/plate_service.py` com funções equivalentes a `ActivatePlateUseCase.execute()`, `DeleteUserPlateUseCase.execute()` e `DeleteVotingPlateUseCase.execute()`
- MUST atualizar `core/viewset.py` removendo imports de `ActivatePlateUseCase`, `DeleteUserPlateUseCase` e `DeleteVotingPlateUseCase`
- MUST substituir instanciação de repositories por acesso direto ao ORM onde aplicável
- MUST preservar contratos HTTP de todos os endpoints de chapa (activate, delete user plate, delete voting plate)
- MUST NOT alterar models, serializers, URLs ou permissões
- MUST rodar `uv run pytest` após a migração
</requirements>

## Subtasks
- [ ] 4.1 Ler os três use cases de plate e mapear suas dependências de port/repository
- [ ] 4.2 Criar `core/services/plate_service.py` com as três funções equivalentes
- [ ] 4.3 Atualizar imports em `core/viewset.py` para usar `plate_service`
- [ ] 4.4 Remover instanciações de `PlateRepository`, `PlateUserRepository`, `VotingPlateRepository` do viewset se não forem mais usadas
- [ ] 4.5 Rodar `uv run pytest` e confirmar ausência de regressão

## Implementation Details
Arquivos de origem:
- `core/use_cases/activite_plate_use_case.py` — usa `PlateRepositoryPort`
- `core/use_cases/delete_plate_user_use_case.py` — usa `CandidateRepositoryPort` e `PlateUserRepositoryPort`
- `core/use_cases/delete_voting_plate_use_case.py` — usa `VotingPlateRepositoryPort`

Arquivo alvo: `core/services/plate_service.py`
- Acessa modelos via `core.models.models` diretamente
- Sem herança de Port

Verificar se `PlateRepository`, `PlateUserRepository`, `VotingPlateRepository` ainda serão necessários após esta task.

### Relevant Files
- `core/use_cases/activite_plate_use_case.py` — lógica de ativação a ser migrada
- `core/use_cases/delete_plate_user_use_case.py` — lógica de exclusão de usuário de chapa
- `core/use_cases/delete_voting_plate_use_case.py` — lógica de exclusão de chapa de votação
- `core/repositories/plate_repository.py` — pode ser substituído por ORM direto
- `core/repositories/plate_user_repository.py` — pode ser substituído por ORM direto
- `core/repositories/voting_plate_repository.py` — pode ser substituído por ORM direto

### Dependent Files
- `core/viewset.py` — três imports serão removidos/substituídos
- `core/services/plate_service.py` — arquivo a ser criado

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/services/plate_service.py` criado com as três funções
- `core/viewset.py` atualizado sem os três use cases de plate
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão
- Endpoints de chapa preservam contratos HTTP

## Tests
- Unit tests:
  - [ ] `plate_service.activate_plate()` com plate válida retorna plate ativada
  - [ ] `plate_service.activate_plate()` com plate inexistente lança exceção
  - [ ] `plate_service.delete_user_plate()` remove associação candidato-chapa corretamente
  - [ ] `plate_service.delete_voting_plate()` remove chapa de votação corretamente
  - [ ] `plate_service.delete_voting_plate()` com chapa inexistente lança exceção
- Integration tests:
  - [ ] `POST /plates/{id}/activate/` retorna 200 com plate ativada
  - [ ] `DELETE /plate-users/{id}/` retorna 204
  - [ ] `DELETE /voting-plates/{id}/` retorna 204
- Test coverage target: >=80%
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `ActivatePlateUseCase`, `DeleteUserPlateUseCase`, `DeleteVotingPlateUseCase` não importados em `core/viewset.py`
- Contratos HTTP de endpoints de chapa preservados
- Nenhuma regressão em outros endpoints
