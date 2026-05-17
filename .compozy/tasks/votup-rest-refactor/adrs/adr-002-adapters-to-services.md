# ADR-002: Migrar Adapters de Infraestrutura para core/services/

## Status

Accepted

## Date

2026-05-16

## Context

O projeto possui dois adapters de infraestrutura:
- `core/adapters/pdf/reportlab_pdf_adapter.py` — geração de PDF via Reportlab
- `core/adapters/storage/file_storage_adapter.py` — upload/download de arquivos no S3

Esses adapters implementam ports (`pdf_generator_port.py`, `file_storage_port.py`) para desacoplar infraestrutura do domínio. Com a remoção da arquitetura hexagonal, os ports perdem utilidade e os adapters precisam ser relocalizados.

## Decision

Os adapters serão migrados diretamente para `core/services/`, renomeados como serviços utilitários:
- `reportlab_pdf_adapter.py` → `core/services/report_service.py`
- `file_storage_adapter.py` → `core/services/storage_service.py`

Os ports correspondentes (`pdf_generator_port.py`, `file_storage_port.py`) serão removidos. Os services chamarão `reportlab` e `django-storages/boto3` diretamente, sem interface intermediária.

## Alternatives Considered

### Alternative 1: core/integrations/ directory

- **Description**: Manter adapters em diretório separado (`core/integrations/`) para preservar isolamento de infraestrutura
- **Pros**: Distinção clara entre lógica de domínio e integrações externas
- **Cons**: Introduz mais um diretório que não existe no padrão Django/DRF convencional; aumenta navegação sem benefício proporcional
- **Why rejected**: A estrutura alvo já prevê `report_service.py` e `storage_service.py` em `core/services/`. O isolamento é suficiente pelo nome do arquivo.

### Alternative 2: Chamar bibliotecas diretamente nos ViewSets

- **Description**: Usar `reportlab` e `django-storages` sem camada de abstração
- **Pros**: Elimina uma camada; código mais direto
- **Cons**: Viola a regra de não colocar lógica pesada em ViewSets; dificulta reutilização e testes
- **Why rejected**: Services são o local adequado para lógica de integração reutilizável.

## Consequences

### Positive

- Estrutura de serviços unificada sob `core/services/`
- Nenhum port/adapter a manter; lógica de integração em um lugar só
- Nomenclatura semântica (`report_service`, `storage_service`) facilita descoberta

### Negative

- Sem interface formal, substituir a implementação de PDF ou storage no futuro exige modificar os services diretamente
- Testes de integração precisam mockar `reportlab`/`boto3` em vez de um port

### Risks

- Risco baixo: as implementações são simples wrappers e a lógica de negócio não reside neles
