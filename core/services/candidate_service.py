"""
core/services/candidate_service.py — Lógica de candidatos (migrada de use_cases)

Substitui UpdateCandidateAvatarUseCase, CandidateRepository e uso direto de
core.models.models para operações de Candidate.

Padrão: funções simples acessando o ORM diretamente (sem Port/Repository intermediário).
"""

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from core.models import models


def update_avatar(candidate_id: int, file_content: bytes, filename: str):
    """Atualiza o avatar de um candidato via ImageField (S3).

    Se o candidato já possuir um avatar, o arquivo anterior é deletado
    automaticamente pelo Django antes do novo upload.

    Args:
        candidate_id: ID do candidato no banco de dados.
        file_content: Conteúdo binário do arquivo de avatar.
        filename: Nome do arquivo para salvar.

    Raises:
        Http404: Se o candidato não existir.
    """
    candidate = get_object_or_404(models.Candidate, pk=candidate_id)
    candidate.avatar.save(filename, ContentFile(file_content), save=True)
