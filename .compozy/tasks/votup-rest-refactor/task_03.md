---
status: completed
title: Migrar lógica de candidatos
type: refactor
complexity: medium
dependencies:
  - task_02
---

# Task 03: Migrar lógica de candidatos

## Overview
Mover a lógica de `UpdateCandidateAvatarUseCase` para `core/services/candidate_service.py` ou `core/services/storage_service.py`. Atualizar os imports em `core/viewset.py` para apontar para o novo service. O contrato HTTP (método, URL, resposta) deve ser preservado integralmente.

<critical>
- SEMPRE LER `core/use_cases/update_candidate_avatar_use_case.py` antes de começar
- REFERÊNCIAR o inventário da task_01 para confirmar quais outros arquivos importam este use case
- FOCO NO "O QUÊ" — mover lógica, não reescrevê-la
- MINIMIZAR CÓDIGO — manter a lógica idêntica à atual
- TESTES REQUERIDOS — endpoint de avatar DEVE continuar funcionando
</critical>

<requirements>
- MUST criar `core/services/candidate_service.py` com função equivalente a `UpdateCandidateAvatarUseCase.execute()`
- MUST atualizar `core/viewset.py` para importar de `core.services.candidate_service` em vez de `core.use_cases.update_candidate_avatar_use_case`
- MUST preservar assinatura de resposta HTTP do endpoint de atualização de avatar
- MUST confirmar que `S3FileStorageAdapter` ainda é usado corretamente (ou movido para `storage_service`)
- MUST NOT alterar models, serializers ou URLs
- MUST rodar `uv run python manage.py check` e `uv run pytest` após a migração
</requirements>

## Subtasks
- [x] 3.1 Ler `core/use_cases/update_candidate_avatar_use_case.py` e entender a lógica atual
- [x] 3.2 Criar `core/services/candidate_service.py` com a lógica equivalente sem usar Port/Repository
- [x] 3.3 Atualizar import em `core/viewset.py` de `UpdateCandidateAvatarUseCase` para o novo service
- [x] 3.4 Confirmar que nenhum outro arquivo importa `UpdateCandidateAvatarUseCase` (conforme inventário)
- [x] 3.5 Rodar `uv run pytest` para confirmar ausência de regressão

## Implementation Details
Arquivo atual: `core/use_cases/update_candidate_avatar_use_case.py`
- Importa `CandidateRepositoryPort` e `FileStoragePort`
- Usa `CandidateRepository` e `S3FileStorageAdapter` como implementações concretas

Arquivo alvo: `core/services/candidate_service.py`
- Acessa o ORM diretamente via `core.models.models`
- Usa `S3FileStorageAdapter` diretamente sem passar por port

Consultar `core/adapters/storage/file_storage_adapter.py` para entender a interface do adaptador.

### Relevant Files
- `core/use_cases/update_candidate_avatar_use_case.py` — lógica a ser migrada
- `core/repositories/candidate_repository.py` — pode ser substituído por acesso direto ao ORM
- `core/adapters/storage/file_storage_adapter.py` — mantido como está
- `core/ports/candidate_repository_port.py` — será dispensado após migração
- `core/ports/file_storage_port.py` — será dispensado após migração

### Dependent Files
- `core/viewset.py` — import de `UpdateCandidateAvatarUseCase` será substituído
- `core/services/candidate_service.py` — arquivo a ser criado

### Related ADRs
Nenhum ADR existente.

## Deliverables
- `core/services/candidate_service.py` criado com lógica de atualização de avatar
- `core/viewset.py` atualizado com novo import
- `uv run python manage.py check` passa
- `uv run pytest` passa sem regressão
- Endpoint `PATCH /candidates/{id}/avatar/` continua respondendo corretamente

## Tests
- Unit tests:
  - [ ] `candidate_service.update_avatar()` com candidato existente e arquivo válido retorna sucesso
  - [ ] `candidate_service.update_avatar()` com candidato inexistente lança exceção apropriada
  - [ ] `candidate_service.update_avatar()` falha de upload no S3 propaga erro correto
- Integration tests:
  - [ ] `PATCH /candidates/{id}/avatar/` com payload válido retorna 200 e URL do avatar atualizada
  - [ ] `PATCH /candidates/{id}/avatar/` sem autenticação retorna 401/403
- Test coverage target: >=80%
- All tests must pass

## Success Criteria
- All tests passing
- Test coverage >=80%
- `UpdateCandidateAvatarUseCase` não é mais importado em `core/viewset.py`
- Endpoint de avatar continua funcionando com mesmo contrato HTTP
- Nenhuma regressão em outros endpoints
