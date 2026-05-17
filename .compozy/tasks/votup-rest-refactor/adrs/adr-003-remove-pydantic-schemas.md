# ADR-003: Eliminar Pydantic Schemas e usar DRF Serializers

## Status

Accepted

## Date

2026-05-16

## Context

`core/schemas/` contém schemas Pydantic (v2) usados para validação e estruturação de dados em use cases e repositories. Com a remoção da arquitetura hexagonal, use cases deixam de existir como camada separada. DRF Serializers já fornecem validação e serialização no contexto de ViewSets e Services.

## Decision

Todos os Pydantic schemas em `core/schemas/` serão eliminados. Onde validação estruturada for necessária fora do contexto HTTP, será usada diretamente a validação do DRF Serializer (chamando `.is_valid()` com `raise_exception=True`) ou dicts simples. A dependência `pydantic` pode ser mantida no `pyproject.toml` apenas se outros módulos do projeto ainda a utilizarem.

## Alternatives Considered

### Alternative 1: Manter schemas Pydantic onde ainda têm imports ativos

- **Description**: Remoção conservadora — apenas schemas sem referências são deletados
- **Pros**: Menor risco de quebra imediata; migração incremental
- **Cons**: Mantém duas ferramentas de validação no projeto sem necessidade; prolonga a coexistência de padrões incompatíveis
- **Why rejected**: A migração completa é o objetivo. Coexistir aumenta a confusão.

### Alternative 2: Converter para dataclasses Python

- **Description**: Substituir Pydantic por `@dataclass` onde um tipo estruturado é necessário
- **Pros**: Zero dependência externa; typing nativo
- **Cons**: Sem validação automática de campos; mais código manual para validar tipos
- **Why rejected**: DRF Serializers já resolvem o problema de validação; dataclasses seriam uma terceira ferramenta desnecessária.

## Consequences

### Positive

- Ecossistema de validação unificado em DRF
- Redução de dependências e arquivos no projeto
- Padrão Django/DRF convencional sem surpresas para novos devs

### Negative

- Se algum schema Pydantic tiver lógica de validação complexa, essa lógica deve ser portada manualmente para Serializers
- Pydantic v2 oferece performance de parsing superior a DRF Serializers em cenários de alta volumetria (não aplicável aqui)

### Risks

- Risco de regressão se schemas Pydantic tiverem imports não mapeados no levantamento inicial; mitigado pelo passo 1 do plano (mapear todos imports).
