# TechSpec: Remoção da Arquitetura Hexagonal — votup-back

## Executive Summary

O `core/` app do votup-back mantém uma camada hexagonal (domain, ports, adapters, repositories, use_cases, dto) que aumentou a complexidade sem benefício proporcional para o tamanho atual do projeto. Esta refatoração remove essas camadas e adota o padrão Django/DRF convencional: **ViewSets → Services/Actions/Behaviors → Models**.

O trade-off central é **menor isolamento formal de infraestrutura** em troca de **menor número de arquivos, imports e pontos de falha**. Rotas públicas, contratos de resposta e migrations não são alterados. O `account/` app já está no padrão alvo e não é tocado.

---

## System Architecture

### Component Overview

**Estado atual (`core/`):**

```
core/
  domain/          → Entidades de domínio (duplicam Models)
  dto/             → DTOs (duplicam Serializers)
  ports/           → Interfaces (pdf_generator_port, file_storage_port, repository ports)
  adapters/        → Implementações (ReportlabPdfAdapter, FileStorageAdapter)
  repositories/    → Acesso a dados (CandidateRepository, PlateRepository, ...)
  use_cases/       → Orquestração de negócio (activite_plate, voter_use_case, generate_pdf/...)
  schemas/         → Pydantic schemas
  models/          → Django Models (manter)
  serializer/      → DRF Serializers (manter)
  viewset.py       → DRF ViewSets (manter, simplificar)
  urls.py          → Routing (não alterar)
  managers.py      → Django Managers (manter)
  filters.py       → DRF FilterSets (manter)
  signals/         → Django Signals (manter)
  exceptions.py    → Exceções customizadas (manter)
  mixins.py        → Mixins DRF (manter)
  utils.py         → Utilitários (manter)
```

**Estado alvo (`core/`):**

```
core/
  models/          → Django Models (sem alteração)
  serializer/      → DRF Serializers (expandir conforme necessário)
  services/
    __init__.py
    candidate_service.py    → Lógica de candidatos (ex-repositories + use_cases)
    plate_service.py        → Lógica de chapas
    voting_service.py       → Lógica de votação
    voting_plate_service.py → Lógica de chapa+votação
    voting_user_service.py  → Lógica de usuário votante
    report_service.py       → Geração de PDF (ex-adapter Reportlab)
    storage_service.py      → Upload/download S3 (ex-adapter FileStorage)
  actions.py       → Operações atômicas e pontuais (ex: activate_plate, delete_vote)
  behaviors.py     → Fluxos compostos multi-etapa (ex: gerar PDF + upload S3 + retornar URL)
  viewset.py       → ViewSets delegando para services/actions/behaviors
  urls.py          → Routing (sem alteração)
  managers.py      → Managers (sem alteração)
  filters.py       → FilterSets (sem alteração)
  signals/         → Signals (sem alteração)
  exceptions.py    → Exceções (sem alteração)
  mixins.py        → Mixins (sem alteração)
  utils.py         → Utilitários (sem alteração)
```

**Fluxo de dados após refatoração:**

```
HTTP Request
    → ViewSet (validação via Serializer)
        → Service / Action / Behavior
            → Django ORM (Model / Manager / QuerySet)
                ↕
            → report_service (Reportlab) | storage_service (S3)
    → Response (Serializer)
```

---

## Implementation Design

### Core Interfaces

Contrato padrão dos services: funções simples (sem classe base obrigatória). Services são módulos Python com funções; não há interface formal — a interface é o conjunto de funções públicas do módulo.

```python
# core/services/candidate_service.py
from core.models.models import Candidate

def get_candidates_for_plate(plate_id: int) -> list[Candidate]:
    return list(Candidate.objects.filter(plate_id=plate_id).select_related("plate"))

def create_candidate(plate_id: int, name: str, number: int) -> Candidate:
    return Candidate.objects.create(plate_id=plate_id, name=name, number=number)

def delete_candidate(candidate_id: int) -> None:
    Candidate.objects.filter(pk=candidate_id).delete()
```

```python
# core/services/report_service.py
from io import BytesIO
from reportlab.pdfgen import canvas  # chamada direta, sem port

def generate_plate_pdf(plate_id: int) -> BytesIO:
    buffer = BytesIO()
    # lógica atual de ReportlabPdfAdapter migrada aqui
    return buffer
```

```python
# core/viewset.py — padrão de ViewSet após refatoração
from rest_framework.decorators import action
from rest_framework.response import Response
from core.services import plate_service, report_service
from core.serializer.serializers import PlateSerializer

class PlateViewSet(viewsets.ModelViewSet):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer

    @action(detail=True, methods=["get"])
    def report(self, request, pk=None):
        pdf = report_service.generate_plate_pdf(plate_id=pk)
        return FileResponse(pdf, content_type="application/pdf")
```

### Data Models

Os Django Models existentes em `core/models/models.py` não são alterados. Serão as únicas representações de dados após remoção de:
- `core/domain/` → domain entities removidas
- `core/dto/` → DTOs removidos; substituídos por Serializers ou dicts simples
- `core/schemas/` → Pydantic schemas removidos; substituídos por DRF Serializers

### API Endpoints

Nenhum endpoint público será alterado. O roteamento em `core/urls.py` e os nomes de actions DRF são preservados. A refatoração é interna — contratos de request/response e paths HTTP permanecem idênticos.

---

## Integration Points

### AWS S3 (django-storages / boto3)

- **Destino**: `core/services/storage_service.py`
- **Auth**: configuração via `settings.py` (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME) — sem alteração
- **Uso atual**: FileStorageAdapter; após migração, `storage_service` chama `django-storages` diretamente

### Reportlab (geração de PDF)

- **Destino**: `core/services/report_service.py`
- **Uso atual**: ReportlabPdfAdapter; após migração, `report_service` instancia `canvas.Canvas` diretamente

---

## Impact Analysis

| Componente | Tipo de Impacto | Descrição e Risco | Ação Necessária |
|---|---|---|---|
| `core/domain/` | Deprecated → Removido | Entidades redundantes com Models. Risco: imports não mapeados | Mapear imports; remover após confirmação |
| `core/dto/` | Deprecated → Removido | DTOs duplicam Serializers. Risco: imports não mapeados | Mapear imports; substituir por Serializers/dicts |
| `core/ports/` | Deprecated → Removido | Interfaces sem implementação após remoção de adapters | Remover após migrar implementações |
| `core/adapters/` | Deprecated → Migrado | Lógica migrada para `services/report_service.py` e `services/storage_service.py` | Migrar lógica; remover diretório |
| `core/repositories/` | Deprecated → Removido | Acesso a dados migrado para services com ORM direto | Migrar queries para services; remover |
| `core/use_cases/` | Deprecated → Migrado | Orquestração migrada para services/actions/behaviors | Mapear; migrar; remover |
| `core/schemas/` | Deprecated → Removido | Pydantic schemas substituídos por DRF Serializers | Migrar validações; remover |
| `core/services/` | Novo | Módulo criado para conter toda lógica de negócio | Criar diretório e arquivos |
| `core/actions.py` | Modificado ou Novo | Operações pontuais migradas de use cases simples | Criar/expandir |
| `core/behaviors.py` | Modificado ou Novo | Fluxos compostos (relatório, PDF+upload) | Criar/expandir |
| `core/viewset.py` | Modificado | ViewSets simplificados para delegar a services | Refatorar chamadas internas |
| `README.md` | Modificado | Remoção de menção à arquitetura hexagonal | Atualizar documentação |

---

## Testing Approach

### Strategy

A validação é feita ao final da migração completa (conforme decisão do usuário). O critério de aceite é:
1. `uv run python manage.py check` passa sem erros
2. Suite de testes existente (`core/tests.py`, `account/tests.py`) passa sem regressões
3. Endpoints validados manualmente ou via Swagger UI (`/api/schema/swagger-ui/`)

### Unit Tests

- Não há exigência de novos testes por service durante a migração
- Testes existentes que testem diretamente use_cases ou repositories devem ser atualizados para chamar os novos services
- Mocks de `boto3` / `reportlab` permanecem nos testes de integração existentes

### Integration Tests

- Testar o fluxo completo: ViewSet → Service → ORM para cada recurso migrado
- Verificar que respostas HTTP mantêm o mesmo shape (status code, campos JSON)
- Testar geração de PDF e upload de arquivo após migração dos adapters

---

## Development Sequencing

### Build Order

A migração é **incremental por módulo** (ADR-002): cada service é criado e validado com `uv run python manage.py check` antes de passar ao próximo. O código hexagonal antigo coexiste até que todos os imports sejam removidos.

1. **Mapear todos os imports antigos** — nenhuma dependência prévia. Usar `grep -r "from core.use_cases\|from core.repositories\|from core.domain\|from core.ports\|from core.adapters\|from core.dto\|from core.schemas" .` para gerar tabela origem→destino.

2. **Criar `core/services/` e arquivos vazios** — depende do passo 1. Criar `__init__.py` e os 7 módulos de service sem lógica ainda.

3. **Migrar `candidate_service.py`** — depende do passo 2. Absorver `update_candidate_avatar_use_case.py` e queries do `CandidateRepository`. Atualizar viewset. Rodar `manage.py check`.

4. **Migrar `plate_service.py`** — depende do passo 3. Absorver `activite_plate_use_case.py`, `check_plate_associate_use_case.py` e `PlateRepository`. Atualizar viewset. Rodar check.

5. **Migrar `voting_service.py`** — depende do passo 4. Absorver `voter_use_case.py` e queries do repositório de EventVoting. Atualizar viewset. Rodar check.

6. **Migrar `voting_plate_service.py`** — depende do passo 5. Absorver `delete_voting_plate_use_case.py` e `VotingPlateRepository`. Atualizar viewset. Rodar check.

7. **Migrar `voting_user_service.py`** — depende do passo 6. Absorver `delete_plate_user_use_case.py` e `PlateUserRepository`. Atualizar viewset. Rodar check.

8. **Criar `storage_service.py`** — depende do passo 2 (independente dos passos 3–7). Absorver `FileStorageAdapter` e `file_storage_port.py`. Rodar check.

9. **Criar `report_service.py`** — depende dos passos 7 e 8. Absorver `ReportlabPdfAdapter`, ports de PDF, e toda a lógica do app `reports/`. Consolidar em `core/services/` (ADR-003). Remover `reports/` de `INSTALLED_APPS`. Rodar check.

10. **Expandir `actions.py` e `behaviors.py`** — depende dos passos 3–9. Mover operações atômicas isoladas para `actions.py`; mover fluxos compostos (ex: `generate_and_upload_voting_report`) para `behaviors.py`.

11. **Deletar código morto** — depende do passo 10. Remover `core/domain/`, `core/dto/`, `core/schemas/`, `core/ports/`, `core/adapters/`, `core/repositories/`, `core/use_cases/`. Confirmar zero imports antes de cada deleção. Rodar check.

12. **Atualizar README** — depende do passo 11. Remover menções à arquitetura hexagonal; documentar nova estrutura de services.

### Technical Dependencies

- Nenhuma dependência de infraestrutura externa: a refatoração é puramente interna
- `uv` deve estar disponível para executar `uv run python manage.py check`
- Banco PostgreSQL local ou variáveis de ambiente configuradas para rodar os testes

---

## Monitoring and Observability

Esta refatoração não altera comportamento em produção. Não há novos endpoints, jobs ou integrações. Observabilidade existente (logs Django, erros Sentry se configurado) permanece sem alteração.

---

## Technical Considerations

### Known Risks

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Import não mapeado causa `ImportError` em runtime | Média | Passo 1 obrigatório: grep completo antes de remover qualquer arquivo |
| Lógica em domain entity não replicada no service | Baixa | Ler cada entity e confirmar que é só estrutura de dados antes de remover |
| Use case com lógica transacional complexa difícil de mapear para service simples | Baixa | Usar `behaviors.py` para fluxos compostos em vez de forçar tudo em service |
| Testes que importam diretamente de use_cases / repositories quebram | Alta | Atualizar imports de teste no passo 9 junto com a correção de regressões |

---

## Architecture Decision Records

- [ADR-001: Remover Arquitetura Hexagonal e adotar Service Layer Django/DRF](adrs/adr-001-remove-hexagonal.md) — Decisão central: substituir camadas hexagonais por ViewSets, Services, Actions, Behaviors e Models.
- [ADR-002: Estratégia de Migração Incremental por Módulo](adrs/adr-002-incremental-migration-strategy.md) — Migração feita módulo a módulo com `manage.py check` a cada etapa; evita big-bang em codebase sem cobertura de testes.
- [ADR-003: Consolidação do módulo reports/ em core/services/](adrs/adr-003-reports-consolidation.md) — Lógica de PDF e S3 migrada para `report_service.py` e `storage_service.py`; app `reports/` removido de INSTALLED_APPS.
