---
status: completed
title: Migrar lógica de votação
type: refactor
complexity: medium
dependencies:
  - task_05
---

# Task 06: Migrar lógica de votação

## Overview
Revisar `core/use_cases/actions.py` e `core/use_cases/behaviors.py`. Manter as classes `VotingAction`, `VotingUserAction` e `VoteByPlateBehavior` se fizerem sentido como estão, ou extrair a regra de negócio reutilizável para `core/services/voting_service.py`. O objetivo é remover dependências de Port/Repository sem alterar o comportamento dos endpoints de votação.

<critical>
- SEMPRE LER `core/use_cases/actions.py` e `core/use_cases/behaviors.py` antes de começar
- REFERÊNCIAR inventário da task_01 — `actions` e `behaviors` são importados diretamente no viewset
- FOCO NO "O QUÊ" — reduzir acoplamento a camadas hexagonais, não reescrever a lógica
- MINIMIZAR CÓDIGO — se actions/behaviors não dependem de Port/Repository, podem permanecer onde estão
- TESTES REQUERIDOS — fluxo completo de votação deve continuar funcionando
</critical>

<requirements>
- MUST verificar se `actions.py` e `behaviors.py` importam de `core.ports` ou `core.repositories` diretamente (conforme inventário)
- MUST remover quaisquer dependências de Port/Repository de `actions.py` e `behaviors.py`, substituindo por acesso direto ao ORM via `core.models`
- SHOULD extrair para `core/services/voting_service.py` qualquer lógica reutilizável que não pertença a um action/behavior de viewset
- MUST preservar a interface pública usada em `core/viewset.py` (ex: `VoteByPlateBehavior`, `actions.VotingAction`)
- MUST NOT alterar o comportamento dos endpoints de votação
- MUST rodar `uv run pytest` após as alterações
</requirements>

## Subtasks
- [ ] 6.1 Ler `core/use_cases/actions.py` e `core/use_cases/behaviors.py` e verificar dependências de Port/Repository
- [ ] 6.2 Se há dependências de Port/Repository: remover e substituir por ORM direto
- [ ] 6.3 Se há lógica reutilizável: extrair para `core/services/voting_service.py`
- [ ] 6.4 Confirmar que `core/viewset.py` continua importando `actions` e `behaviors` sem erros
- [ ] 6.5 Rodar `uv run pytest` e confirmar ausência de regressão

## Implementation Details
Arquivos de origem (podem permanecer no lugar ou ser movidos):
- `core/use_cases/actions.py` — importa `core.models`, não usa Port/Repository diretamente (confirmar)
- `core/use_cases/behaviors.py` — importa `core.models`, não usa Port/Repository diretamente (confirmar)

Se nenhum dos dois importar Port/Repository, esta tarefa é de baixa complexidade — apenas confirmar e documentar.

Se houver dependências: criar `core/services/voting_service.py` seguindo o mesmo padrão das tasks anteriores.

### Relevant Files
- `core/use_cases/actions.py` — ações de votação (pode permanecer ou ser refatorado)
- `core/use_cases/behaviors.py` — comportamento de votação por chapa (pode permanecer ou ser refatorado)
- `core/use_cases/voter_use_case.py` — `GetVoter` use case importado no viewset

### Dependent Files
- `core/viewset.py` — importa `actions`, `behaviors`, `VoteByPlateBehavior`, `GetVoter`
- `core/services/voting_service.py` — criado apenas se necessário

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/use_cases/actions.py` e `core/use_cases/behaviors.py` sem dependências de Port/Repository (ou confirmação que já não as tinham)
- `core/services/voting_service.py` criado somente se necessário
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão

## Tests
- Unit tests:
  - [ ] `VotingAction.execute()` com voto válido registra voto corretamente
  - [ ] `VotingUserAction.execute()` com usuário já votado retorna erro de conflito
  - [ ] `VoteByPlateBehavior.execute()` com chapa inativa retorna erro esperado
  - [ ] `GetVoter.execute()` com voter existente retorna dados corretos
- Integration tests:
  - [ ] Endpoint de votação (`POST /votes/`) com payload válido retorna 200/201
  - [ ] Endpoint de votação com chapa inativa retorna erro esperado
- Test coverage target: >=80%
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `core/use_cases/actions.py` e `core/use_cases/behaviors.py` sem imports de Port/Repository
- Endpoints de votação preservam comportamento atual
- Nenhuma regressão em outros endpoints
