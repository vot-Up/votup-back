# ADR-001: Remover Arquitetura Hexagonal e adotar Service Layer Django/DRF

## Status

Accepted

## Contexto

O projeto votup-back foi implementado com uma estrutura inspirada em Arquitetura Hexagonal, usando pastas como domain, ports, adapters, repositories, use_cases e dto.

Para o tamanho atual do projeto, essa separação aumentou a complexidade, criou muitos arquivos intermediários e tornou alterações simples mais lentas.

O projeto é um backend Django REST Framework. A estrutura desejada agora é mais direta, usando ViewSets, Serializers, Models, Managers, Services, Actions e Behaviors.

## Decisão

Vamos remover gradualmente a arquitetura hexagonal e adotar uma arquitetura Django/DRF mais direta:

- ViewSets como controllers HTTP.
- Serializers para entrada, saída e validação.
- Models e Managers para persistência e queries.
- Services para regras de negócio reutilizáveis.
- Actions para operações pontuais.
- Behaviors para fluxos mais longos, especialmente relatórios, PDFs e processos compostos.

## Consequências positivas

- Menos camadas para navegar.
- Menos arquivos boilerplate.
- Mais aderente ao padrão comum de projetos Django/DRF.
- Mais fácil para novos devs entenderem.
- Refatorações futuras ficam mais diretas.

## Consequências negativas

- Menor isolamento formal entre domínio e infraestrutura.
- Algumas regras de negócio podem ficar mais próximas do Django ORM.
- Exige disciplina para não colocar lógica demais nos ViewSets.

## Regras da refatoração

- Não mudar endpoints públicos sem necessidade.
- Não alterar models ou migrations sem necessidade.
- Não apagar código antes de confirmar que não há imports.
- Não mover lógica pesada para ViewSet se ela puder ficar em service/action/behavior.
- Cada etapa deve passar em `uv run python manage.py check`.
- Sempre que possível, preservar ou adicionar testes.
