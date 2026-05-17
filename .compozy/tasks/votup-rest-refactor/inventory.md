# Inventário da Arquitetura Hexagonal — votup-back

> **Data:** 2025-05-16  
> **Propósito:** Mapear todos os imports de camadas hexagonais antes da refatoração (Tarefa 01).  
> **Nenhum arquivo de código foi alterado.**

---

## 1. Arquivos por Camada Hexagonal

### 1.1 `core/domain/` — Entidades de domínio

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | `__init__.py` | Init vazio |
| 2 | `candidate.py` | Entidade Candidate |
| 3 | `plate.py` | Entidade Plate |
| 4 | `plate_user.py` | Entidade PlateUser |
| 5 | `voter.py` | Entidade Voter |
| 6 | `voting_plate.py` | Entidade VotingPlate |

### 1.2 `core/ports/` — Interfaces/Portas

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | `__init__.py` | Init vazio |
| 2 | `candidate_repository_port.py` | Importa `core.domain.candidate` |
| 3 | `file_storage_port.py` | Interface de armazenamento |
| 4 | `plate_repository_port.py` | Importa `core.domain.plate` |
| 5 | `plate_user_repository_port.py` | Interface de repositório PlateUser |
| 6 | `voter_repository_repository_port.py` | Importa `core.domain.voter` |
| 7 | `voting_plate_repository_port.py` | Interface de repositório VotingPlate |
| 8 | `pdf/__init__.py` | Init vazio |
| 9 | `pdf/pdf_generator_port.py` | Interface de geração PDF |

### 1.3 `core/adapters/` — Adaptadores concretos

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | `__init__.py` | Init vazio |
| 2 | `pdf/__init__.py` | Init vazio |
| 3 | `pdf/reportlab_pdf_adapter.py` | Implementa `PdfGeneratorPort` |
| 4 | `storage/__init__.py` | Init vazio |
| 5 | `storage/file_storage_adapter.py` | S3FileStorageAdapter |

### 1.4 `core/repositories/` — Acesso a dados

| # | Arquivo | Descrição | Imports hex. |
|---|---------|-----------|--------------|
| 1 | `__init__.py` | Init vazio | — |
| 2 | `candidate_repository.py` | CandidateRepository | `domain.candidate`, `ports.candidate_repository_port` |
| 3 | `plate_repository.py` | PlateRepository | `domain.plate`, `ports.plate_repository_port` |
| 4 | `plate_user_repository.py` | PlateUserRepository | `ports.plate_user_repository_port` |
| 5 | `report_repository.py` | ReportRepository | `ports.pdf.pdf_generator_port` |
| 6 | `voter_repository.py` | VoterRepository | `domain.voter`, `ports.voter_repository_repository_port` |
| 7 | `voting_plate_repository.py` | VotingPlateRepository | `ports.voting_plate_repository_port` |

### 1.5 `core/use_cases/` — Casos de uso / Orquestração

| # | Arquivo | Descrição | Imports hex. |
|---|---------|-----------|--------------|
| 1 | `__init__.py` | Init vazio | — |
| 2 | `actions.py` | VotingUserAction, EventVotingAction, ResumeVoteAction | — |
| 3 | `activite_plate_use_case.py` | ActivatePlateUseCase | `ports.plate_repository_port` |
| 4 | `behaviors.py` | VoteByPlateBehavior, VotingUserBehavior, ResumeVoterProvisory | — |
| 5 | `check_plate_associate_use_case.py` | CheckPlateAssociateUseCase | `ports.voting_plate_repository_port` |
| 6 | `delete_plate_user_use_case.py` | DeleteUserPlateUseCase | `ports.candidate_repository_port`, `ports.plate_user_repository_port` |
| 7 | `delete_voting_plate_use_case.py` | DeleteVotingPlateUseCase | `ports.voting_plate_repository_port` |
| 8 | `update_candidate_avatar_use_case.py` | UpdateCandidateAvatarUseCase | `ports.candidate_repository_port`, `ports.file_storage_port` |
| 9 | `voter_use_case.py` | GetVoter | `ports.voter_repository_repository_port` |
| 10 | `generate_pdf/__init__.py` | Init vazio | — |
| 11 | `generate_pdf/base_pdf_use_case.py` | BasePdfUseCase | `ports.pdf.pdf_generator_port` |
| 12 | `generate_pdf/generate_general_vote_result_pdf_service.py` | GenerateGeneralVoteResultPdfService | — |
| 13 | `generate_pdf/generate_general_vote_result_use_case.py` | GenerateGeneralVoteResultUseCase | `ports.pdf.pdf_generator_port`, `use_cases.generate_pdf.*` |

### 1.6 `core/dto/` — Data Transfer Objects

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | `__init__.py` | Init vazio |
| 2 | `candidate_dto.py` | CandidateDTO |
| 3 | `plate_dto.py` | PlateDTO |
| 4 | `plate_user_dto.py` | PlateUserDTO |
| 5 | `voter_dto.py` | VoterDTO |
| 6 | `voting_plate_dto.py` | VotingPlateDTO |

### 1.7 `core/schemas/` — Pydantic Schemas

| # | Arquivo | Descrição |
|---|---------|-----------|
| 1 | `schemas.py` | REPORT_SCHEMAS, VOTER_SCHEMAS, VOTING_SCHEMAS, AUTH_SCHEMAS, USER_SCHEMAS |

---

## 2. Mapa de Imports — `core/viewset.py`

Imports hexagonais diretos em `core/viewset.py` (linhas 15–34):

```
│
├── core/adapters/storage/file_storage_adapter.py
│   └── S3FileStorageAdapter
│
├── core/dto/voter_dto.py
│   └── VoterDTO
│
├── core/repositories/candidate_repository.py
│   └── CandidateRepository
│
├── core/repositories/plate_repository.py
│   └── PlateRepository
│
├── core/repositories/plate_user_repository.py
│   └── PlateUserRepository
│
├── core/repositories/report_repository.py
│   └── ReportRepository
│
├── core/repositories/voter_repository.py
│   └── VoterRepository
│
├── core/repositories/voting_plate_repository.py
│   └── VotingPlateRepository
│
├── core.schemas.schemas
│   └── REPORT_SCHEMAS, VOTER_SCHEMAS, VOTING_SCHEMAS
│
├── core.use_cases (módulo)
│   ├── actions
│   │   └── VotingUserAction, EventVotingAction, ResumeVoteAction
│   └── behaviors
│       └── VoteByPlateBehavior, VotingUserBehavior, ResumeVoterProvisory, VoterInPlateResume
│
├── core.use_cases.activite_plate_use_case
│   └── ActivatePlateUseCase
│
├── core.use_cases.behaviors
│   └── VoteByPlateBehavior
│
├── core.use_cases.check_plate_associate_use_case
│   └── CheckPlateAssociateUseCase
│
├── core.use_cases.delete_plate_user_use_case
│   └── DeleteUserPlateUseCase
│
├── core.use_cases.delete_voting_plate_use_case
│   └── DeleteVotingPlateUseCase
│
├── core.use_cases.generate_pdf.generate_general_vote_result_use_case
│   └── GenerateGeneralVoteResultUseCase
│
├── core.use_cases.update_candidate_avatar_use_case
│   └── UpdateCandidateAvatarUseCase
│
└── core.use_cases.voter_use_case
    └── GetVoter
```

### Onde cada import de `core/viewset.py` é usado

| Import | Origin | Usado em qual ViewSet/action |
|--------|--------|------------------------------|
| `S3FileStorageAdapter` | adapters/storage | `CandidateViewSet.upload_avatar` |
| `VoterDTO` | dto | `VoterViewSet.can_vote` |
| `CandidateRepository` | repositories | `CandidateViewSet.upload_avatar`, `PlateUserViewSet.delete_user_plate` |
| `PlateRepository` | repositories | `PlateViewSet.update` |
| `PlateUserRepository` | repositories | `PlateUserViewSet.delete_user_plate` |
| `ReportRepository` | repositories | `VotingUserViewSet.resume_report` |
| `VoterRepository` | repositories | `VoterViewSet.can_vote` |
| `VotingPlateRepository` | repositories | `VotingPlateViewSet.delete_voting_plate`, `VotingPlateViewSet.check_associate` |
| `REPORT_SCHEMAS / VOTER_SCHEMAS / VOTING_SCHEMAS` | schemas | Decorators `@extend_schema_view` em VotingUserViewSet, VoterViewSet, VotingViewSet |
| `actions` (módulo) | use_cases | `VotingViewSet.active_vote`, `VotingViewSet.close_vote`, `VotingUserViewSet.voting` |
| `behaviors` (módulo) | use_cases | `VotingUserViewSet.get_voting_user_plate_quantity_pdf`, `VotingUserViewSet.resume_report_plate_vote`, `VotingUserViewSet.get_voter_plate_pdf`, `ResumeVoteViewSet.resume_report` |
| `ActivatePlateUseCase` | use_cases | `PlateViewSet.update` |
| `VoteByPlateBehavior` | use_cases | `VotingUserViewSet.resume_report_plate_vote` |
| `CheckPlateAssociateUseCase` | use_cases | `VotingPlateViewSet.check_associate` |
| `DeleteUserPlateUseCase` | use_cases | `PlateUserViewSet.delete_user_plate` |
| `DeleteVotingPlateUseCase` | use_cases | `VotingPlateViewSet.delete_voting_plate` |
| `GenerateGeneralVoteResultUseCase` | use_cases | `VotingUserViewSet.resume_report` |
| `UpdateCandidateAvatarUseCase` | use_cases | `CandidateViewSet.upload_avatar` |
| `GetVoter` | use_cases | `VoterViewSet.can_vote` |

---

## 3. Imports Hexagonais Fora de `core/`

A única referência externa a camadas hexagonais é em **`account/viewset.py`** (linhas 10–11):

```python
from core.schemas.schemas import AUTH_SCHEMAS, USER_SCHEMAS  # usado em autenticação
from core.viewset import ViewSetBase, ViewSetPermissions     # classes base de ViewSet
```

> **Nota:** Nenhum arquivo de `reports/` ou de outros apps importa diretamente de `core/` — o app `reports` é chamado indiretamente por viewsets ou UseCases.

---

## 4. Cross-References: Quais arquivos hexagonais são importados por quê

### 4.1 Cadeamentos de imports internos às camadas hexagonais

```
core/ports/pdf/pdf_generator_port.py
  (nenhum import de core.)

core/ports/candidate_repository_port.py
  └── core.domain.candidate

core/ports/plate_repository_port.py
  └── core.domain.plate

core/ports/voter_repository_repository_port.py
  └── core.domain.voter

core/adapters/pdf/reportlab_pdf_adapter.py
  └── core.ports.pdf.pdf_generator_port

core/adapters/storage/file_storage_adapter.py
  (nenhum import de core.)

core/repositories/candidate_repository.py
  ├── core.domain.candidate
  ├── core.ports.candidate_repository_port
  └── core.models

core/repositories/plate_repository.py
  ├── core.domain.plate
  ├── core.ports.plate_repository_port
  └── core.models

core/repositories/voter_repository.py
  ├── core.domain.voter
  ├── core.ports.voter_repository_repository_port
  └── core.models

core/repositories/report_repository.py
  └── core.ports.pdf.pdf_generator_port

core/repositories/plate_user_repository.py
  ├── core.ports.plate_user_repository_port
  └── core.models

core/repositories/voting_plate_repository.py
  ├── core.ports.voting_plate_repository_port
  └── core.models

core/use_cases/activite_plate_use_case.py
  └── core.ports.plate_repository_port

core/use_cases/check_plate_associate_use_case.py
  └── core.ports.voting_plate_repository_port

core/use_cases/delete_plate_user_use_case.py
  ├── core.ports.candidate_repository_port
  └── core.ports.plate_user_repository_port

core/use_cases/delete_voting_plate_use_case.py
  └── core.ports.voting_plate_repository_port

core/use_cases/update_candidate_avatar_use_case.py
  ├── core.ports.candidate_repository_port
  └── core.ports.file_storage_port

core/use_cases/voter_use_case.py
  └── core.ports.voter_repository_repository_port

core/use_cases/generate_pdf/generate_general_vote_result_use_case.py
  └── core.ports.pdf.pdf_generator_port

core/dto/voter_dto.py
  (nenhum import de camada hexagonal)
```

### 4.2 Nenhum cross-reference externa confirmada

`account/viewset.py` importa de `core.schemas` e `core.viewset` — nenhuma camada hexagonal profunda é acessada diretamente por apps externos. Todos os repositórios, use-cases, adapters e DTOs são consumidos **exclusivamente** dentro de `core/`.

---

## 5. Candidatos à Remoção (não usados diretamente em `core/viewset.py` e não importados por apps externos)

### 5.1 `core/domain/` — TODOS os arquivos
O viewset não importa diretamente `core.domain.*`. Os domain entities são importadas apenas por ports e repositories, que também são removidas posteriormente.

| Arquivo | Status | Motivo |
|---------|--------|--------|
| `domain/candidate.py` | 🗑️ Candidato à remoção | Sem import em viewset ou app externo |
| `domain/plate.py` | 🗑️ Candidato à remoção | Sem import em viewset ou app externo |
| `domain/plate_user.py` | 🗑️ Candidato à remoção | Sem import em viewset ou app externo |
| `domain/voter.py` | 🗑️ Candidato à remoção | Sem import em viewset ou app externo |
| `domain/voting_plate.py` | 🗑️ Candidato à remoção | Sem import em viewset ou app externo |

### 5.2 `core/dto/` — TODOS os arquivos
Apenas `dto/voter_dto.py` é importado pelo viewset (VoterDTO). Os demais nunca são importados.

| Arquivo | Status | Motivo |
|---------|--------|--------|
| `dto/candidate_dto.py` | 🗑️ Candidato à remoção | Nunca importado |
| `dto/plate_dto.py` | 🗑️ Candidato à remoção | Nunca importado |
| `dto/plate_user_dto.py` | 🗑️ Candidato à remoção | Nunca importado |
| `dto/voter_dto.py` | ⚠️ Usado em viewset | Importado em `VoterViewSet.can_vote` — requires migration before removal |
| `dto/voting_plate_dto.py` | 🗑️ Candidato à remoção | Nunca importado |

### 5.3 `core/ports/` — TODOS os arquivos
Nenhuma porta é importada diretamente pelo viewset — todas são reachables apenas via repositories e use_cases.

| Arquivo | Status | Motivo |
|---------|--------|--------|
| `ports/candidate_repository_port.py` | 🗑️ Candidato à remoção | Usado por repositories e use_cases; não diretamente em viewset |
| `ports/file_storage_port.py` | 🗑️ Candidato à remoção | Usado por use_case de avatar; não diretamente em viewset |
| `ports/plate_repository_port.py` | 🗑️ Candidato à remoção | Usado por repository e use_case; não diretamente em viewset |
| `ports/plate_user_repository_port.py` | 🗑️ Candidato à remoção | Usado por repository e use_case; não diretamente em viewset |
| `ports/voter_repository_repository_port.py` | 🗑️ Candidato à remoção | Usado por repository e use_case; não diretamente em viewset |
| `ports/voting_plate_repository_port.py` | 🗑️ Candidato à remoção | Usado por repositories/use_cases; não diretamente em viewset |
| `ports/pdf/pdf_generator_port.py` | 🗑️ Candidato à remoção | Usado por report_repository e use_cases de PDF; não em viewset diretamente |

### 5.4 `core/adapters/` — TODOS os arquivos

| Arquivo | Status | Motivo |
|---------|--------|--------|
| `adapters/pdf/reportlab_pdf_adapter.py` | 🗑️ Candidato à remoção | Usado por report_repository; não em viewset diretamente |
| `adapters/storage/file_storage_adapter.py` | ⚠️ Usado em viewset | `S3FileStorageAdapter` importado diretamente em `core/viewset.py` — requires migration before removal |

### 5.5 `core/repositories/` — TODOS os arquivos
Todos os 6 repositórios são importados diretamente em `core/viewset.py` — **todos são "usados"**.

| Arquivo | Status | Motivo |
|---------|--------|--------|
| `repositories/candidate_repository.py` | ✅ Usado em viewset | `CandidateRepository` → CandidateViewSet, PlateUserViewSet |
| `repositories/plate_repository.py` | ✅ Usado em viewset | `PlateRepository` → PlateViewSet |
| `repositories/plate_user_repository.py` | ✅ Usado em viewset | `PlateUserRepository` → PlateUserViewSet |
| `repositories/report_repository.py` | ✅ Usado em viewset | `ReportRepository` → VotingUserViewSet |
| `repositories/voter_repository.py` | ✅ Usado em viewset | `VoterRepository` → VoterViewSet |
| `repositories/voting_plate_repository.py` | ✅ Usado em viewset | `VotingPlateRepository` → VotingPlateViewSet |

### 5.6 `core/use_cases/` — Análise individual

| Arquivo | Usado em viewset? | Status |
|---------|-------------------|--------|
| `use_cases/actions.py` | Sim — VotingUserAction, EventVotingAction, ResumeVoteAction | ✅ Usado |
| `use_cases/behaviors.py` | Sim — VoteByPlateBehavior, VotingUserBehavior, ResumeVoterProvisory, VoterInPlateResume | ✅ Usado |
| `use_cases/activite_plate_use_case.py` | Sim — ActivatePlateUseCase em PlateViewSet | ✅ Usado |
| `use_cases/check_plate_associate_use_case.py` | Sim — CheckPlateAssociateUseCase em VotingPlateViewSet | ✅ Usado |
| `use_cases/delete_plate_user_use_case.py` | Sim — DeleteUserPlateUseCase em PlateUserViewSet | ✅ Usado |
| `use_cases/delete_voting_plate_use_case.py` | Sim — DeleteVotingPlateUseCase em VotingPlateViewSet | ✅ Usado |
| `use_cases/update_candidate_avatar_use_case.py` | Sim — UpdateCandidateAvatarUseCase em CandidateViewSet | ✅ Usado |
| `use_cases/voter_use_case.py` | Sim — GetVoter em VoterViewSet | ✅ Usado |
| `use_cases/generate_pdf/generate_general_vote_result_use_case.py` | Sim — GenerateGeneralVoteResultUseCase em VotingUserViewSet | ✅ Usado |
| `use_cases/generate_pdf/generate_general_vote_result_pdf_service.py` | ✅ Usado em use case irmão | ✅ Usado (indiretamente) |
| `use_cases/generate_pdf/base_pdf_use_case.py` | ⚠️ Não importado diretamente por viewset | ⚠️ Verificar se usado por generator_service |

### 5.7 `core/schemas/schemas.py`

| Arquivo | Usado fora de core? | Status |
|---------|--------------------|--------|
| `schemas/schemas.py` | Sim — `account/viewset.py` | ⚠️ Usado esp. externamente |

---

## 6. Sumário por Categoria

### ✅ Usados diretamente em `core/viewset.py`
| Categoria | Arquivos |
|-----------|---------|
| `core/repositories/` | Todos os 6 arquivos |
| `core/use_cases/` | 10 arquivos (actions, behaviors, 8 use cases específicos) |
| `core/adapters/` | `storage/file_storage_adapter.py` |
| `core/dto/` | `voter_dto.py` |
| `core/schemas/` | `schemas.py` (viewset.py, remoto) |

### ⚠️ Usados por apps externos (não só core/viewset.py)
| Categoria | Arquivos |
|-----------|---------|
| `core/schemas/` | `schemas.py` (importado em `account/viewset.py`) |

### 🗑️ Candidatos à remoção sem uso em viewset ou apps externos
| Categoria | Arquivos |
|-----------|---------|
| `core/domain/` | Todos (5 arquivos) |
| `core/dto/` | `candidate_dto.py`, `plate_dto.py`, `plate_user_dto.py`, `voting_plate_dto.py` |
| `core/ports/` | Todos (5 arquivos + 1 sub) |
| `core/adapters/` | `pdf/reportlab_pdf_adapter.py` |
| `core/repositories/` | Enquanto viewset os usa, são todos candidatos após migração |
| `core/use_cases/` | Enquanto viewset os usa, são todos candidatos após migração |
| `core/schemas/` | `schemas.py` (candidato após migrar schemas para serializers, mas depende de conta a usuário) |

### ⚠️ Usado em viewset, mas前提下 (pré-requisito) antes de remover
| Categoria | Arquivo | Razão |
|-----------|---------|-------|
| `core/dto/` | `voter_dto.py` | Importado diretamente por `VoterViewSet.can_vote` |
| `core/adapters/` | `storage/file_storage_adapter.py` | Instanciado em `CandidateViewSet.upload_avatar` |
| `core/schemas/` | `schemas.py` | Importado por `account/viewset.py` — validar após migração |

---

## 7. Dependências entre Camadas Hexagonais

```
domain (entidades) ← ports (interfaces)
                              ↓
                         adapters
                         repositories ← ports, domain, models
                         use_cases ← ports, geradores_pdf

                         viewset.py ← repositories, use_cases, adapters, dto, schemas
                         account (externo) ← schemas, viewset base
```

---

## 8. Validação

**Comando:** `uv run python manage.py check`

```
System check identified no issues (0 silenced).
```

✅ `uv run python manage.py check` passa sem erros. Nenhuma alteração estava em andamento.

### Outros arquivos Python envolvidos (não hexagonais)

| Arquivo | Descrição |
|---------|-----------|
| `core/models/__init__.py` | Exporta todos os models Django |
| `core/models/models.py` | Django ORM Models — manter intactas |
| `core/serializer/serializers.py` | DRF Serializers — a serem expandidas |
| `core/filters.py` | DRF FilterSets — manter |
| `core/managers.py` | Managers Django — manter |
| `core/mixins.py` | Mixins de ViewSet — manter |
| `core/exceptions.py` | Exceções customizadas — manter |
| `core/messages.py` | Constantes de mensagem — manter |
| `core/urls.py` | Routing — manter |
| `core/mixins.py` | Mixins — manter |
| `core.params_serializer.py` | Serializers de parâmetros — manter |
| `core/tests.py` | Testes — manter |

---

*Este arquivo é um snapshot do estado atual. Ele deve ser atualizado conforme a refatoração avança (cada arquivo removido deve ter sua remoção registrada aqui).*
