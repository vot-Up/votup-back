"""
core/services/storage_service.py — Lógica de armazenamento S3 (migrada de adapters)

Fornece funções simples que encapsulam S3FileStorageAdapter.
Sem Port/Repository intermediário.
"""

from core.adapters.storage.file_storage_adapter import S3FileStorageAdapter


def upload_file(file: bytes, filename: str) -> str:
    """Faz upload de um arquivo para o S3 e retorna a URL.

    Args:
        file: Conteúdo binário do arquivo.
        filename: Nome do arquivo no S3.

    Returns:
        str com a URL do arquivo uploaded.
    """
    storage = S3FileStorageAdapter()
    return storage.upload(file, filename)


def delete_file(file_url: str) -> None:
    """Deleta um arquivo do S3 pela URL.

    Args:
        file_url: URL do arquivo a ser deletado.
    """
    storage = S3FileStorageAdapter()
    storage.delete(file_url)
