# ADR-003: Consolidação do módulo reports/ em core/services/

## Status

Accepted

## Date

2026-05-16

## Context

O projeto tem um módulo reports/ separado com ports e adapters para geração de PDF (ReportLab) e armazenamento (S3). Com a remoção da arquitetura hexagonal, manter reports/ como app Django independente criaria uma inconsistência: o core/ estaria sem hexagonal, mas reports/ ainda teria a estrutura antiga de ports/adapters.

## Decision

Migrar a lógica do módulo reports/ para core/services/report_service.py e core/services/storage_service.py. O app reports/ Django é removido ou reduzido a uma camada mínima (urls.py e viewset.py), delegando toda a lógica de negócio para os services do core/.

## Alternatives Considered

### Alternative 1: Manter reports/ como app Django separado

- **Description**: reports/ permanece como app independente, mas sem ports/adapters internos.
- **Pros**: Separação de responsabilidades clara; reports/ pode escalar independentemente.
- **Cons**: Inconsistência com a estrutura alvo; dois lugares para lógica de relatórios.
- **Why rejected**: Fragmenta a lógica de negócio e contradiz a estrutura alvo definida pelo time.

### Alternative 2: Manter reports/ com ports/adapters internos

- **Description**: reports/ permanece com a estrutura hexagonal intacta.
- **Pros**: Sem mudança no módulo reports/.
- **Cons**: Contradiz diretamente o objetivo da refatoração.
- **Why rejected**: Incoerente com a decisão ADR-001.

## Consequences

### Positive

- Lógica de relatórios centralizada em core/services/, alinhada com a estrutura alvo.
- Menos apps Django para gerenciar.
- Adapters de PDF e storage viram services utilitários reutilizáveis.

### Negative

- report_service.py e storage_service.py terão dependências de bibliotecas externas (ReportLab, boto3) dentro do core/.
- Requer atualizar INSTALLED_APPS se reports/ for removido.

### Risks

- Se reports/ tiver migrations próprias, precisam ser consolidadas ou preservadas. Mitigação: verificar migrations antes de remover o app.

## Implementation Notes

- `file_storage_adapter.py` → `core/services/storage_service.py`
- `reportlab_pdf_adapter.py` → `core/services/report_service.py`
- Ports de PDF e storage são removidos junto com os adapters.

## References

- [ADR-001: Remover Arquitetura Hexagonal](adr-001-remove-hexagonal.md)
- [ADR-002: Estratégia de Migração Incremental](adr-002-incremental-migration-strategy.md)
