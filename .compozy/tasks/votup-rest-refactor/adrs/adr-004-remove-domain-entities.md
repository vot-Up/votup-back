# ADR-004: Remover Domain Entities e usar Django Models diretamente

## Status

Accepted

## Date

2026-05-16

## Context

`core/domain/` contém entidades de domínio (Candidate, Plate, Voter, PlateUser, VotingPlate) que espelham os Django Models em `core/models/`. Essas entidades foram criadas para isolar o domínio da persistência, padrão da arquitetura hexagonal. Na prática, são classes Python simples (dataclasses ou namedtuples) sem lógica de negócio não-trivial — apenas estruturas de dados que duplicam os Models.

## Decision

Todas as domain entities em `core/domain/` serão removidas. Services e ViewSets operarão diretamente sobre instâncias de Django Model e QuerySets. Nenhuma camada de mapeamento entre Model e entity será criada.

## Alternatives Considered

### Alternative 1: Manter domain entities com lógica de negócio não-trivial

- **Description**: Preservar entidades que contenham validações ou comportamentos próprios além de estrutura de dados
- **Pros**: Separa lógica de domínio do ORM
- **Cons**: Exige mapeamento bidirecional model↔entity em cada operação; aumenta boilerplate
- **Why rejected**: A exploração do código revelou que as entidades são estruturas de dados sem lógica própria. O custo de manter o mapeamento supera o benefício.

### Alternative 2: Converter para dataclasses (sem persistência)

- **Description**: Transformar domain entities em `@dataclass` Python puras para manter tipos explícitos
- **Pros**: Typing claro; sem dependência do ORM nas classes de domínio
- **Cons**: Cria uma terceira representação dos mesmos dados (model + entity + serializer)
- **Why rejected**: Django Models com type hints e Serializers já fornecem contratos suficientemente explícitos.

## Consequences

### Positive

- Uma única representação de dados: o Django Model
- Elimina mapeamento model↔entity em todos os use cases
- Reduz número de arquivos e imports

### Negative

- Lógica de negócio fica mais próxima do Django ORM; trocar de banco no futuro seria mais trabalhoso (risco hipotético)
- Disciplina necessária para não colocar lógica de ORM dentro de ViewSets

### Risks

- DTOs em `core/dto/` que dependem das domain entities devem ser removidos junto (coberto pelo plano de refatoração)
- Risco de regressão em lógica que dependa de campos calculados nas entities: mitigado pelo mapeamento de imports na etapa 1.
