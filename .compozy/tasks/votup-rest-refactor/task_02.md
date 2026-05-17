---
status: completed
title: Criar estrutura base de services
type: refactor
complexity: low
dependencies:
  - task_01
---

# Task 02: Criar estrutura base de services

## Overview
Criar o diretório `core/services/` com `__init__.py` e definir o padrão que os services seguirão no projeto. Nenhuma lógica de negócio é migrada aqui — apenas a estrutura vazia e o padrão de nomenclatura são estabelecidos para que as tasks seguintes possam referenciar.

<critical>
- SEMPRE LER o inventário produzido na task_01 antes de começar
- NÃO ALTERAR comportamento — apenas criar estrutura vazia
- FOCO NO "O QUÊ" — estrutura de diretórios e padrão de service
- MINIMIZAR CÓDIGO — `__init__.py` vazio ou com imports básicos
- TESTES REQUERIDOS — confirmar que o projeto ainda sobe após a criação
</critical>

<requirements>
- MUST criar `core/services/__init__.py`
- MUST garantir que nenhum import existente é quebrado
- MUST confirmar que `uv run python manage.py check` passa após a criação
- SHOULD documentar brevemente o padrão de service em comentário no `__init__.py` ou em `core/services/README.md`
- MUST NOT mover nenhuma lógica de negócio nesta tarefa
</requirements>

## Subtasks
- [x] 2.1 Criar `core/services/__init__.py` vazio
- [x] 2.2 Confirmar que `uv run python manage.py check` passa sem erros
- [x] 2.3 Confirmar que `uv run pytest` não quebra testes existentes

## Implementation Details
Estrutura alvo:
```
core/
  services/
    __init__.py
```

O padrão de service será: funções simples ou classes sem herança de Port/Repository. Dependências são injetadas via parâmetros ou acessam o ORM diretamente.

### Relevant Files
- `core/services/__init__.py` — arquivo a ser criado

### Dependent Files
- `core/viewset.py` — importará os services nas tasks seguintes (não alterado aqui)

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/services/__init__.py` criado
- `uv run python manage.py check` passa
- `uv run pytest` passa (sem regressão)

## Tests
- Unit tests:
  - [x] `uv run python manage.py check` retorna 0 erros após criação do diretório
- Integration tests:
  - [x] `uv run pytest` passa sem regressão (nenhuma lógica foi alterada)
- Test coverage target: N/A (tarefa de criação de estrutura)
- All tests must pass

## Success Criteria
- All tests passing
- `core/services/` existe no filesystem
- Nenhum import existente quebrado
- Nenhuma lógica de negócio movida
