---
status: completed
title: Remover camadas hexagonais não utilizadas
type: chore
complexity: medium
dependencies:
  - task_03
  - task_04
  - task_05
  - task_06
  - task_07
---

# Task 08: Remover camadas hexagonais não utilizadas

## Overview
Após todas as migrações, remover os arquivos de `core/use_cases/`, `core/repositories/`, `core/ports/`, `core/adapters/`, `core/domain/` e `core/dto/` que não possuem mais nenhum import em produção. Cada remoção deve ser precedida de um grep confirmando ausência de imports.

<critical>
- SEMPRE EXECUTAR grep antes de remover qualquer arquivo
- NÃO REMOVER arquivos que ainda são importados em qualquer lugar
- FOCO NO "O QUÊ" — limpar código morto, não refatorar o que sobrou
- MINIMIZAR RISCO — remover um grupo de arquivos por vez e testar
- TESTES REQUERIDOS — `uv run pytest` deve passar após cada grupo de remoções
</critical>

<requirements>
- MUST executar `grep -rn "from core.<camada>" --exclude-dir=.venv` para cada arquivo antes de remover
- MUST NOT remover nenhum arquivo que ainda tenha imports ativos
- MUST remover apenas arquivos identificados como "não usados" no inventário da task_01 e confirmados como não importados após as tasks 03-07
- MUST rodar `uv run pytest` após cada grupo de remoções
- MUST confirmar que `uv run python manage.py check` passa ao final
- SHOULD remover diretórios vazios após remoção de todos os arquivos dentro deles
</requirements>

## Subtasks
- [ ] 8.1 Executar grep completo para confirmar ausência de imports dos use cases migrados
- [ ] 8.2 Remover use cases migrados: `update_candidate_avatar_use_case.py`, `activite_plate_use_case.py`, `delete_plate_user_use_case.py`, `delete_voting_plate_use_case.py`, `check_plate_associate_use_case.py`, `generate_general_vote_result_use_case.py`
- [ ] 8.3 Rodar `uv run pytest` após remoção de use cases
- [ ] 8.4 Executar grep para confirmar ausência de imports dos repositories dispensados
- [ ] 8.5 Remover repositories sem mais importers (conforme inventário atualizado)
- [ ] 8.6 Rodar `uv run pytest` após remoção de repositories
- [ ] 8.7 Executar grep para confirmar ausência de imports de ports e domain dispensados
- [ ] 8.8 Remover ports, domain, dto sem importers (conforme inventário)
- [ ] 8.9 Rodar `uv run pytest` e `uv run python manage.py check` final

## Implementation Details
Grupos de remoção (na ordem sugerida):

**Grupo 1 — Use Cases migrados:**
- `core/use_cases/update_candidate_avatar_use_case.py`
- `core/use_cases/activite_plate_use_case.py`
- `core/use_cases/delete_plate_user_use_case.py`
- `core/use_cases/delete_voting_plate_use_case.py`
- `core/use_cases/check_plate_associate_use_case.py`
- `core/use_cases/generate_pdf/generate_general_vote_result_use_case.py`
- `core/use_cases/generate_pdf/base_pdf_use_case.py`
- `core/use_cases/generate_pdf/generate_general_vote_result_pdf_service.py`

**Grupo 2 — Repositories (confirmar via grep):**
- `core/repositories/candidate_repository.py`
- `core/repositories/plate_repository.py`
- `core/repositories/plate_user_repository.py`
- `core/repositories/report_repository.py`
- `core/repositories/voter_repository.py`
- `core/repositories/voting_plate_repository.py`

**Grupo 3 — Ports, Domain, DTO (confirmar via grep):**
- `core/ports/` (todos os arquivos não importados)
- `core/domain/` (todos os arquivos não importados)
- `core/dto/` (todos os arquivos não importados)

**ATENÇÃO:** `actions.py` e `behaviors.py` dentro de `core/use_cases/` podem permanecer se ainda forem importados no viewset (conforme task_06).

### Relevant Files
- Todos os arquivos listados nos grupos acima — sujeitos a remoção mediante confirmação de grep

### Dependent Files
- `core/viewset.py` — deve estar limpo de todos os imports hexagonais após as tasks 03-07
- `core/services/` — deve conter toda a lógica migrada

### Related ADRs
Nenhum ADR existente.

## Deliverables
- Todos os arquivos hexagonais não utilizados removidos
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão
- `grep "from core\.(use_cases|repositories|ports|domain|dto)" core/viewset.py` retorna 0 resultados (exceto se actions/behaviors permaneceram)

## Tests
- Unit tests:
  - [ ] `uv run python manage.py check` retorna 0 erros após cada grupo de remoções
- Integration tests:
  - [ ] `uv run pytest` passa completamente após remoção de cada grupo
  - [ ] Grep confirma ausência de imports dos arquivos removidos em todo o projeto
- Test coverage target: N/A (tarefa de remoção de código morto)
- All tests must pass

## Success Criteria
- All tests passing
- Nenhum import quebrado após remoções
- `uv run python manage.py check` retorna 0 erros
- Diretórios de camadas hexagonais vazios (ou com apenas `__init__.py` + arquivos ainda usados)
- `core/viewset.py` importa apenas de `core.services`, `core.use_cases.actions`, `core.use_cases.behaviors`
