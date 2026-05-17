---
status: completed
title: Migrar geração de relatórios e PDF
type: refactor
complexity: high
dependencies:
  - task_02
---

# Task 07: Migrar geração de relatórios e PDF

## Overview
Mover a lógica de geração de PDF e relatórios de `core/use_cases/generate_pdf/` e `core/repositories/report_repository.py` para `core/services/report_service.py`. Atualizar imports em `core/viewset.py`. Os endpoints de relatório devem continuar retornando os mesmos PDFs e dados.

<critical>
- SEMPRE LER `core/use_cases/generate_pdf/generate_general_vote_result_use_case.py`, `core/use_cases/generate_pdf/base_pdf_use_case.py` e `core/repositories/report_repository.py` antes de começar
- REFERÊNCIAR inventário da task_01 para mapear todos os imports de generate_pdf
- FOCO NO "O QUÊ" — migrar lógica de geração, não reescrever algoritmo de PDF
- MINIMIZAR CÓDIGO — `ReportlabPdfAdapter` deve continuar sendo o adaptador de PDF
- TESTES REQUERIDOS — endpoints de relatório devem retornar PDFs válidos após migração
</critical>

<requirements>
- MUST criar `core/services/report_service.py` com lógica equivalente a `GenerateGeneralVoteResultUseCase.execute()`
- MUST atualizar `core/viewset.py` removendo import de `GenerateGeneralVoteResultUseCase`
- MUST manter `core/adapters/pdf/reportlab_pdf_adapter.py` como implementação concreta de geração de PDF
- MUST substituir uso de `ReportRepositoryPort` por chamada direta ao adaptador ou ORM
- MUST preservar contratos HTTP dos endpoints de relatório (content-type, status codes, estrutura do PDF)
- MUST NOT alterar a lógica de geração do conteúdo do PDF
- MUST rodar `uv run pytest` após a migração
</requirements>

## Subtasks
- [ ] 7.1 Ler todo o módulo `core/use_cases/generate_pdf/` e `core/repositories/report_repository.py`
- [ ] 7.2 Criar `core/services/report_service.py` com a lógica de geração de relatório/PDF
- [ ] 7.3 Atualizar import de `GenerateGeneralVoteResultUseCase` em `core/viewset.py`
- [ ] 7.4 Confirmar que `ReportRepository` pode ser dispensado (conforme inventário)
- [ ] 7.5 Confirmar que `core/adapters/pdf/reportlab_pdf_adapter.py` continua sendo usado
- [ ] 7.6 Rodar `uv run pytest` e confirmar ausência de regressão

## Implementation Details
Arquivos de origem:
- `core/use_cases/generate_pdf/generate_general_vote_result_use_case.py` — use case principal
- `core/use_cases/generate_pdf/base_pdf_use_case.py` — usa `ReportRepositoryPort`
- `core/use_cases/generate_pdf/generate_general_vote_result_pdf_service.py` — serviço de PDF interno
- `core/repositories/report_repository.py` — implementação de `ReportRepositoryPort`
- `core/adapters/pdf/reportlab_pdf_adapter.py` — adaptador concreto de PDF

Arquivo alvo: `core/services/report_service.py`
- Orquestra geração de dados + geração de PDF via `ReportlabPdfAdapter` diretamente

### Relevant Files
- `core/use_cases/generate_pdf/generate_general_vote_result_use_case.py` — lógica principal a migrar
- `core/use_cases/generate_pdf/base_pdf_use_case.py` — base class com port
- `core/use_cases/generate_pdf/generate_general_vote_result_pdf_service.py` — serviço interno de PDF
- `core/repositories/report_repository.py` — pode ser dispensado após migração
- `core/adapters/pdf/reportlab_pdf_adapter.py` — mantido, referenciado diretamente
- `core/ports/pdf/pdf_generator_port.py` — será dispensado após migração

### Dependent Files
- `core/viewset.py` — import de `GenerateGeneralVoteResultUseCase` será removido
- `core/services/report_service.py` — arquivo a ser criado

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/services/report_service.py` criado com lógica de geração de relatório/PDF
- `core/viewset.py` atualizado sem `GenerateGeneralVoteResultUseCase`
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão
- Endpoints de relatório retornam PDFs válidos com mesmo conteúdo

## Tests
- Unit tests:
  - [ ] `report_service.generate_general_vote_result()` com votação válida retorna bytes de PDF
  - [ ] `report_service.generate_general_vote_result()` com votação vazia retorna PDF com dados zerados
  - [ ] `report_service.generate_general_vote_result()` com votação inexistente lança exceção
- Integration tests:
  - [ ] `GET /reports/general-result/` retorna `Content-Type: application/pdf` e status 200
  - [ ] `GET /reports/general-result/` sem autenticação retorna 401/403
- Test coverage target: >=80%
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `GenerateGeneralVoteResultUseCase` não importado em `core/viewset.py`
- Endpoints de relatório retornam PDFs com mesmo conteúdo de antes
- Nenhuma regressão em outros endpoints
