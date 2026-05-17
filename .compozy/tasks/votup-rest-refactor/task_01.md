---
status: completed
title: Inventariar arquitetura hexagonal atual
type: chore
complexity: low
dependencies: []
---

# Task 01: Inventariar arquitetura hexagonal atual

## Overview
Mapear todos os imports de `core.use_cases`, `core.repositories`, `core.ports`, `core.adapters`, `core.domain` e `core.dto` no codebase. Identificar quais arquivos os consomem e quais são candidatos à remoção futura. Nenhuma linha de código deve ser alterada nesta tarefa.

<critical>
- SEMPRE LER o contexto completo antes de começar
- NÃO MODIFICAR código — apenas inventariar
- FOCO NO "O QUÊ" — produzir um mapa claro do estado atual
- MINIMIZAR CÓDIGO — sem alterações, só leitura e documentação
- TESTES REQUERIDOS — verificar que `uv run python manage.py check` passa sem erros
</critical>

<requirements>
- MUST mapear todos os imports de camadas hexagonais em `core/viewset.py`
- MUST listar todos os arquivos em `core/use_cases/`, `core/repositories/`, `core/ports/`, `core/adapters/`, `core/domain/`, `core/dto/`
- MUST identificar quais use cases/repositories são referenciados no viewset e quais não são
- MUST produzir um relatório em `.compozy/tasks/votup-rest-refactor/inventory.md`
- MUST confirmar que `uv run python manage.py check` passa sem alterações
</requirements>

## Subtasks
- [x] 1.1 Executar grep de todos os imports hexagonais no projeto (excluindo `.venv`)
- [x] 1.2 Listar todos os arquivos existentes em cada camada hexagonal
- [x] 1.3 Identificar quais arquivos são importados em `core/viewset.py`
- [x] 1.4 Identificar arquivos de camadas que NÃO são importados em nenhum lugar fora de `core/`
- [x] 1.5 Documentar o mapa em `inventory.md` na pasta da feature
- [x] 1.6 Confirmar que `uv run python manage.py check` passa sem alterações

## Implementation Details
Nenhum arquivo de código será criado ou modificado. O resultado é um documento de inventário.

Comandos de referência para o inventário:
```
grep -rn "from core\." --include="*.py" --exclude-dir=.venv --exclude-dir=__pycache__
find core/ -name "*.py" -not -path "*__pycache__*" -not -path "*migrations*"
```

### Relevant Files
- `core/viewset.py` — contém todos os imports hexagonais que precisam ser mapeados
- `core/use_cases/` — camada de casos de uso (alvo principal da refatoração)
- `core/repositories/` — camada de repositórios
- `core/ports/` — interfaces/portas da arquitetura hexagonal
- `core/adapters/` — adaptadores concretos
- `core/domain/` — entidades de domínio
- `core/dto/` — data transfer objects

### Dependent Files
- `.compozy/tasks/votup-rest-refactor/inventory.md` — será criado como saída desta tarefa

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `inventory.md` com mapa completo dos imports hexagonais
- Lista de arquivos candidatos à remoção (não importados fora de `core/`)
- Confirmação que `uv run python manage.py check` passa
- Unit tests não aplicáveis (tarefa de análise estática)

## Tests
- Unit tests:
  - [x] `uv run python manage.py check` retorna 0 erros
- Integration tests:
  - [ ] `uv run pytest` não quebra nenhum teste existente após a tarefa (nenhum código foi alterado)
- Test coverage target: N/A (tarefa de leitura)
- All tests must pass

## Success Criteria
- All tests passing
- `inventory.md` criado com mapa completo
- Nenhum arquivo de código modificado
- Lista clara de arquivos hexagonais por categoria: "usado", "não usado"
