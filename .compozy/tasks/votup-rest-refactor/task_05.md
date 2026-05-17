---
status: completed
title: Migrar lógica de associação
type: refactor
complexity: medium
dependencies:
    - task_04
---

# Task 05: Migrar lógica de associação

## Overview
Mover `CheckPlateAssociateUseCase` para `core/services/voting_plate_service.py`. Atualizar imports em `core/viewset.py`. A resposta HTTP do endpoint de verificação de associação deve ser preservada exatamente.

<critical>
- SEMPRE LER `core/use_cases/check_plate_associate_use_case.py` antes de começar
- REFERÊNCIAR inventário da task_01 para confirmar que nenhum outro arquivo importa este use case
- FOCO NO "O QUÊ" — migrar sem alterar comportamento
- MINIMIZAR CÓDIGO — lógica idêntica à atual
- TESTES REQUERIDOS — endpoint de associação deve responder igual ao atual
</critical>

<requirements>
- MUST criar `core/services/voting_plate_service.py` com função equivalente a `CheckPlateAssociateUseCase.execute()`
- MUST atualizar `core/viewset.py` removendo import de `CheckPlateAssociateUseCase`
- MUST preservar a resposta HTTP do endpoint de verificação de associação (status code, campos de resposta)
- MUST substituir uso de `VotingPlateRepositoryPort` por acesso direto ao ORM
- MUST NOT alterar models, serializers ou URLs
- MUST rodar `uv run pytest` após a migração
</requirements>

## Subtasks
- [ ] 5.1 Ler `core/use_cases/check_plate_associate_use_case.py` e mapear dependências
- [ ] 5.2 Criar `core/services/voting_plate_service.py` com função equivalente
- [ ] 5.3 Atualizar import em `core/viewset.py`
- [ ] 5.4 Confirmar que `VotingPlateRepository` já foi tratado na task_04 ou ainda é necessário
- [ ] 5.5 Rodar `uv run pytest` e confirmar ausência de regressão

## Implementation Details
Arquivo de origem: `core/use_cases/check_plate_associate_use_case.py`
- Importa `VotingPlateRepositoryPort`

Arquivo alvo: `core/services/voting_plate_service.py`
- Usa `VotingPlate` model diretamente via `core.models.models`

Se `voting_plate_service.py` já existir por conta da task_04 (improvável mas possível), adicionar a função ao arquivo existente.

### Relevant Files
- `core/use_cases/check_plate_associate_use_case.py` — lógica a ser migrada
- `core/repositories/voting_plate_repository.py` — pode ser dispensado após esta task
- `core/ports/voting_plate_repository_port.py` — será dispensado após migração

### Dependent Files
- `core/viewset.py` — import de `CheckPlateAssociateUseCase` será removido
- `core/services/voting_plate_service.py` — arquivo a ser criado

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/services/voting_plate_service.py` criado com lógica de verificação de associação
- `core/viewset.py` atualizado sem `CheckPlateAssociateUseCase`
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão
- Endpoint de associação preserva contrato HTTP

## Tests
- Unit tests:
  - [ ] `voting_plate_service.check_plate_associate()` com associação existente retorna verdadeiro/dados esperados
  - [ ] `voting_plate_service.check_plate_associate()` com associação inexistente retorna falso/exceção esperada
  - [ ] `voting_plate_service.check_plate_associate()` com IDs inválidos lança exceção apropriada
- Integration tests:
  - [ ] Endpoint de verificação de associação retorna mesma resposta que antes da migração
- Test coverage target: >=80%
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `CheckPlateAssociateUseCase` não importado em `core/viewset.py`
- Resposta HTTP do endpoint de associação preservada
- Nenhuma regressão em outros endpoints
