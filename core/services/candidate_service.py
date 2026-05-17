"""
core/services/candidate_service.py — Lógica de candidatos (migrada de use_cases)

Substitui UpdateCandidateAvatarUseCase, CandidateRepository e uso direto de
core.models.models para operações de Candidate.

Padrão: funções simples acessando o ORM diretamente via storage_service
(sem Port/Repository intermediário).
"""

from django.shortcuts import get_object_or_404

from core.models import models
from core.services import storage_service


def update_avatar(candidate_id: int, file: bytes, filename: str):
    """Atualiza o avatar de um candidato no S3.

    Se o candidato já possuir um avatar, o arquivo anterior é deletado antes
    do novo upload.

    Args:
        candidate_id: ID do candidato no banco de dados.
        file: Conteúdo binário do arquivo de avatar.
        filename: Nome do arquivo para salvar no S3.

    Raises:
        Http404: Se o candidato não existir.
        botocore.exceptions.ClientError: Em falhas de upload/deletação S3.
    """
    candidate = get_object_or_404(models.Candidate, pk=candidate_id)

    if candidate.avatar_url:
        storage_service.delete_file(candidate.avatar_url)

    new_url = storage_service.upload_file(file, filename)
    candidate.avatar_url = new_url
    candidate.save(update_fields=["avatar_url"])
