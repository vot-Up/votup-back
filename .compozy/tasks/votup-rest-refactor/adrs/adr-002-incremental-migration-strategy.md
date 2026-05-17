# ADR-002: Estratégia de Migração Incremental por Módulo

## Status

Accepted

## Date

2026-05-16

## Context

A remoção da arquitetura hexagonal envolve eliminar domain, ports, adapters, repositories, use_cases e dto do módulo core/. São 13 use cases e múltiplos repositories/adapters interconectados. Uma migração abrupta (big-bang) aumenta o risco de regressão e impossibilita rollback parcial.

## Decision

Adotar migração incremental por módulo: cada use_case ou repository é migrado para services/actions/behaviors individualmente. O código hexagonal antigo é mantido até que todos os imports sejam removidos. Cada etapa deve passar em `uv run python manage.py check` antes de prosseguir.

## Alternatives Considered

### Alternative 1: Big-bang (tudo de uma vez)

- **Description**: Remove toda a estrutura hexagonal em um único PR.
- **Pros**: Menos overhead de compatibilidade residual; PR mais limpo.
- **Cons**: Alto risco de regressão; difícil de revisar; rollback complexo.
- **Why rejected**: O projeto não tem cobertura de testes adequada para garantir segurança num big-bang.

### Alternative 2: Migração por camada

- **Description**: Remove primeiro todos os repositories, depois todos os use_cases, depois os adapters.
- **Pros**: Elimina dependências entre camadas de forma ordenada.
- **Cons**: Pode deixar use_cases quebrados temporariamente enquanto repositories são removidos.
- **Why rejected**: Gera estados intermediários inconsistentes, dificultando o `manage.py check` a cada etapa.

## Consequences

### Positive

- Cada etapa é verificável e revertível isoladamente.
- Reduz risco de regressão em produção.
- Permite PRs menores e mais revisáveis.

### Negative

- Período de coexistência entre código hexagonal e novo service layer.
- Importações duplicadas temporárias aumentam a complexidade transitória.

### Risks

- Importações circulares durante a coexistência. Mitigação: mapear todos os imports no início de cada etapa.

## Implementation Notes

Sequência recomendada: candidate_service → plate_service → voting_service → voting_plate_service → voting_user_service → report_service → storage_service. Após cada service, remover o use_case/repository correspondente e verificar com `manage.py check`.

## References

- [ADR-001: Remover Arquitetura Hexagonal](adr-001-remove-hexagonal.md)
