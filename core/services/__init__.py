"""
core/services — Service Layer (ADR-001)

Padrão de service: funções simples ou classes sem herança de Port/Repository.
Dependências são injetadas via parâmetros ou acessam o ORM diretamente.

Camadas hexagonais (domain, ports, adapters, repositories, use_cases) foram
removidas em favor deste padrão Django/DRF convencional.

Módulos de service:
- candidate_service — Lógica de candidatos (avatar upload)
- plate_service — Lógica de chapas/plates (ativar, remover)
- voting_service — Lógica de votação (ativar, encerrar, votar, histórico)
- voting_plate_service — Lógica de associação chapa-votação
- voter_service — Lógica de eleitores (verificação)
- report_service — Geração de PDF (resultado geral)
- storage_service — Upload/download S3
- pdf_behaviors — Comportamentos de geração de PDF por chapa/evento
"""

# Services são importados como módulos, não re-exportados aqui.
# Uso: from core.services import plate_service
