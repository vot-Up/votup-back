# Workflow Memory

Keep only durable, cross-task context here. Do not duplicate facts that are obvious from the repository, PRD documents, or git history.

## Current State
- Tasks 01-08 concluídas: Migração completa de Arquitetura Hexagonal para Service Layer
- `core/services/` agora contém toda a lógica de negócio:
  - candidate_service.py — update_avatar (com storage_service)
  - plate_service.py — activate_plate, delete_user_plate, delete_voting_plate
  - voting_service.py — active_vote, close_vote, delete_historic, get_voting_user, get_voter_plate, get_resume_vote
  - voting_plate_service.py — check_plate_associate
  - voter_service.py — get_voter
  - report_service.py — generate_general_vote_result
  - storage_service.py — upload_file, delete_file
  - pdf_behaviors.py — VotingUserBehavior, VoterInPlateResume, ResumeVoterProvisory, VoteByPlateBehavior
- Camadas hexagonais removidas: ports/, repositories/, domain/, dto/, use_cases/
- `core/viewset.py` importa apenas de core.services, core.models, core.schemas, core.serializer
- 36 testes passam, manage.py check OK
- Coverage dos services: voter_service 100%, voting_plate_service 100%, report_service 93%, plate_service 93%, voting_service 91%

## Shared Decisions
- Referências externas a camadas hexagonais: apenas `account/viewset.py` importa `core.schemas` e `core.viewset` (base classes) — schemas mantido
- `core/adapters/` mantido (S3FileStorageAdapter usado via storage_service, ReportlabPdfAdapter sem herança de Port)
- `core/schemas/schemas.py` é importado por `account/viewset.py` — mantido até migração de account

## Shared Learnings
- `core/schemas/schemas.py` é importado também por `account/viewset.py` — não pode ser removido até que account seja migrado
- `ReportlabPdfAdapter` não era usado em nenhum lugar — era apenas uma abstração nunca referenciada
- behaviors de PDF (VoteByPlateBehavior, etc.) usam SQL raw com `connection.cursor()` — migrados para pdf_behaviors.py
- `VoterDTO` (pydantic) foi substituído por dict direto no voter_service — pydantic era overhead desnecessário

## Open Risks
- `core/schemas/schemas.py` precisa de migração de `account/` antes da remoção
- `core/adapters/` ainda existe — pode ser simplificado futuramente integrando no storage_service diretamente

## Handoffs
- Tasks 09-10 pendentes: atualizar documentação (README já atualizado) e verificação final
