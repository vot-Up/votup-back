---
status: completed
title: Atualizar documentação
type: docs
complexity: low
dependencies:
  - task_08
---

# Task 09: Atualizar documentação

## Overview
Atualizar o `README.md` para remover referências à arquitetura hexagonal e documentar a nova estrutura baseada em `services/`, `actions/` e `behaviors/`. A documentação deve refletir o estado real do projeto após a refatoração.

<critical>
- SEMPRE LER o `README.md` atual antes de editar
- NÃO INVENTAR — documentar apenas o que existe após a refatoração
- FOCO NO "O QUÊ" — descrever a estrutura atual, não justificar as decisões de design
- MINIMIZAR TEXTO — README enxuto é mais útil que README completo mas desatualizado
- TESTES REQUERIDOS — verificar que `uv run python manage.py check` ainda passa (nenhum código foi alterado)
</critical>

<requirements>
- MUST remover ou atualizar qualquer seção do README que mencione "arquitetura hexagonal", "ports and adapters", "use cases", "repositories" ou "domain objects"
- MUST adicionar seção descrevendo a nova estrutura: `core/services/`, `core/use_cases/actions.py`, `core/use_cases/behaviors.py`
- MUST documentar os services criados: `candidate_service.py`, `plate_service.py`, `voting_plate_service.py`, `report_service.py`
- SHOULD manter instruções de setup, execução e testes já existentes no README
- MUST NOT alterar nenhum arquivo Python
</requirements>

## Subtasks
- [ ] 9.1 Ler o `README.md` atual e identificar seções com referências à arquitetura hexagonal
- [ ] 9.2 Remover ou reescrever seções que descrevem ports/adapters/use_cases/repositories/domain
- [ ] 9.3 Adicionar seção "Estrutura" descrevendo `core/services/` e o padrão DRF adotado
- [ ] 9.4 Listar os services existentes com uma linha de descrição cada
- [ ] 9.5 Confirmar que o README não contém referências desatualizadas

## Implementation Details
Arquivo a editar: `README.md` (raiz do projeto)

Estrutura sugerida para a seção nova:
```
## Estrutura do Backend

- `core/services/` — camada de serviços com lógica de negócio
  - `candidate_service.py` — operações sobre candidatos (upload de avatar)
  - `plate_service.py` — ativação e exclusão de chapas
  - `voting_plate_service.py` — verificação de associação a votação
  - `report_service.py` — geração de relatórios e PDFs
- `core/use_cases/actions.py` — ações de votação (VotingAction, VotingUserAction)
- `core/use_cases/behaviors.py` — comportamentos de votação por chapa
```

### Relevant Files
- `README.md` — arquivo a ser editado

### Dependent Files
Nenhum arquivo dependente (apenas documentação).

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `README.md` atualizado sem referências à arquitetura hexagonal
- Seção de estrutura documentando `core/services/`
- `uv run python manage.py check` passa (nenhum código alterado)

## Tests
- Unit tests:
  - [ ] `uv run python manage.py check` retorna 0 erros (confirmar que nenhum Python foi alterado)
- Integration tests:
  - [ ] N/A (tarefa de documentação)
- Test coverage target: N/A
- All tests must pass

## Success Criteria
- All tests passing
- `README.md` não contém "hexagonal", "ports and adapters", "use_cases" como padrão arquitetural
- Seção de estrutura documenta os services criados nas tasks 03-07
- Instruções de setup e execução preservadas e corretas
