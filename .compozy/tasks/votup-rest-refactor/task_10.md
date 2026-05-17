---
status: completed
title: Verificação final e validação
type: chore
complexity: low
dependencies:
  - task_09
---

# Task 10: Verificação final e validação

## Overview
Executar verificação completa do projeto após a refatoração: `uv run python manage.py check`, `uv run pytest`, grep de imports antigos e atualização do status de todas as tasks para `completed`. Garantir que a refatoração não introduziu regressões.

<critical>
- SEMPRE EXECUTAR todos os comandos de verificação — não pular nenhum
- NÃO MODIFICAR código nesta tarefa — apenas verificar e documentar
- FOCO NO "O QUÊ" — estado final do projeto deve estar limpo e funcional
- MINIMIZAR RISCO — qualquer falha deve ser reportada e corrigida antes de marcar como completo
- TESTES REQUERIDOS — todos os testes devem passar antes de finalizar
</critical>

<requirements>
- MUST executar `uv run python manage.py check` e confirmar 0 erros
- MUST executar `uv run pytest` e confirmar 0 falhas
- MUST executar grep de imports antigos e confirmar que `core/viewset.py` não contém imports de `use_cases`, `repositories`, `ports`, `domain`, `dto` (exceto `actions` e `behaviors` se mantidos)
- MUST atualizar status de todas as tasks em `_tasks.md` para `completed`
- SHOULD documentar quaisquer desvios encontrados em relação ao plano original
- MUST NOT fechar esta task com falhas não resolvidas
</requirements>

## Subtasks
- [ ] 10.1 Executar `uv run python manage.py check` e registrar resultado
- [ ] 10.2 Executar `uv run pytest` e registrar resultado (número de testes, falhas, cobertura)
- [ ] 10.3 Executar grep de imports hexagonais em todo o projeto (excluindo `.venv`)
- [ ] 10.4 Confirmar que `core/services/` contém todos os services esperados
- [ ] 10.5 Atualizar status de todas as tasks em `_tasks.md` para `completed`

## Implementation Details
Comandos de verificação a executar em ordem:

```bash
# 1. Check do Django
uv run python manage.py check

# 2. Testes
uv run pytest

# 3. Grep de imports antigos (deve retornar apenas arquivos dentro de core/use_cases/actions.py e behaviors.py)
grep -rn "from core\.use_cases\|from core\.repositories\|from core\.ports\|from core\.domain\|from core\.dto" \
  --include="*.py" --exclude-dir=.venv --exclude-dir=__pycache__

# 4. Confirmar estrutura de services
ls core/services/
```

### Relevant Files
- `core/viewset.py` — deve estar livre de imports hexagonais (exceto actions/behaviors)
- `core/services/` — deve conter todos os services criados
- `.compozy/tasks/votup-rest-refactor/_tasks.md` — status das tasks a atualizar

### Dependent Files
Nenhum arquivo dependente (tarefa de verificação).

### Related ADRs
Nenhum ADR existente.

## Deliverables
- Resultado documentado de `uv run python manage.py check` (0 erros)
- Resultado documentado de `uv run pytest` (0 falhas)
- Grep confirmando ausência de imports hexagonais em `core/viewset.py`
- `_tasks.md` com todas as tasks em status `completed`

## Tests
- Unit tests:
  - [ ] `uv run python manage.py check` retorna 0 erros
  - [ ] `uv run pytest` retorna 0 falhas
- Integration tests:
  - [ ] Grep de `"from core\.(use_cases|repositories|ports|domain|dto)"` em `core/viewset.py` retorna 0 resultados de use cases/ports migrados
- Test coverage target: >=80% (agregado de todas as tasks)
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `uv run python manage.py check` retorna 0 erros
- `uv run pytest` retorna 0 falhas
- Grep confirma que `core/viewset.py` não importa camadas hexagonais migradas
- Todas as tasks de `_tasks.md` estão com status `completed`
- `core/services/` contém `candidate_service.py`, `plate_service.py`, `voting_plate_service.py`, `report_service.py`
